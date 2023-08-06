import pathlib
import pytest
from datetime import timedelta
from neuro_sdk import Client
from textwrap import dedent
from typing import AsyncIterator, Mapping, Optional, Tuple, Union
from yarl import URL

from neuro_flow import ast
from neuro_flow.ast import CacheStrategy, InputType
from neuro_flow.config_loader import BatchLocalCL, ConfigLoader, LiveLocalCL
from neuro_flow.context import (
    EMPTY_ROOT,
    CacheConf,
    DepCtx,
    NotAvailable,
    RunningBatchFlow,
    RunningLiveFlow,
    sanitize_name,
    setup_inputs_ctx,
)
from neuro_flow.expr import (
    EvalError,
    PrimitiveExpr,
    SimpleOptPrimitiveExpr,
    SimpleOptStrExpr,
    SimpleStrExpr,
)
from neuro_flow.parser import ConfigDir
from neuro_flow.tokenizer import Pos
from neuro_flow.types import LocalPath, RemotePath, TaskStatus


def test_inavailable_context_ctor() -> None:
    err = NotAvailable("job")
    assert err.args == ("The 'job' context is not available",)
    assert str(err) == "The 'job' context is not available"


@pytest.fixture
async def live_config_loader(
    loop: None,
    assets: pathlib.Path,
    client: Client,
) -> AsyncIterator[ConfigLoader]:
    config_dir = ConfigDir(
        workspace=assets,
        config_dir=assets,
    )
    cl = LiveLocalCL(config_dir, client)
    yield cl
    await cl.close()


@pytest.fixture
async def batch_config_loader(
    loop: None,
    assets: pathlib.Path,
    client: Client,
) -> AsyncIterator[ConfigLoader]:
    config_dir = ConfigDir(
        workspace=assets,
        config_dir=assets,
    )
    cl = BatchLocalCL(config_dir, client)
    yield cl
    await cl.close()


async def test_ctx_flow(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-minimal")
    ctx = flow._ctx
    assert ctx.flow.flow_id == "live_minimal"
    assert ctx.flow.project_id == "unit"
    assert ctx.flow.workspace == live_config_loader.workspace
    assert ctx.flow.title == "live_minimal"


async def test_env_defaults(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    ctx = flow._ctx
    assert ctx.env == {"global_a": "val-a", "global_b": "val-b"}


async def test_env_from_job(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    job = await flow.get_job("test_a", {})
    assert job.env == {
        "global_a": "val-a",
        "global_b": "val-b",
        "local_a": "val-1",
        "local_b": "val-2",
        "local_c": "val-mixin-3",
    }


async def test_volumes(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    ctx = flow._ctx
    assert ctx.volumes.keys() == {"volume_a", "volume_b"}

    assert ctx.volumes["volume_a"].id == "volume_a"
    assert ctx.volumes["volume_a"].remote == URL("storage:dir")
    assert ctx.volumes["volume_a"].mount == RemotePath("/var/dir")
    assert ctx.volumes["volume_a"].read_only
    assert ctx.volumes["volume_a"].local == LocalPath("dir")
    assert (
        ctx.volumes["volume_a"].full_local_path == live_config_loader.workspace / "dir"
    )
    assert ctx.volumes["volume_a"].ref_ro == "storage:dir:/var/dir:ro"
    assert ctx.volumes["volume_a"].ref_rw == "storage:dir:/var/dir:rw"
    assert ctx.volumes["volume_a"].ref == "storage:dir:/var/dir:ro"

    assert ctx.volumes["volume_b"].id == "volume_b"
    assert ctx.volumes["volume_b"].remote == URL("storage:other")
    assert ctx.volumes["volume_b"].mount == RemotePath("/var/other")
    assert not ctx.volumes["volume_b"].read_only
    assert ctx.volumes["volume_b"].local is None
    assert ctx.volumes["volume_b"].full_local_path is None
    assert ctx.volumes["volume_b"].ref_ro == "storage:other:/var/other:ro"
    assert ctx.volumes["volume_b"].ref_rw == "storage:other:/var/other:rw"
    assert ctx.volumes["volume_b"].ref == "storage:other:/var/other:rw"


async def test_images(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    ctx = flow._ctx
    assert ctx.images.keys() == {"image_a"}

    assert ctx.images["image_a"].id == "image_a"
    assert ctx.images["image_a"].ref == "image:banana"
    assert ctx.images["image_a"].context == live_config_loader.workspace / "dir"
    assert (
        ctx.images["image_a"].dockerfile
        == live_config_loader.workspace / "dir/Dockerfile"
    )
    assert ctx.images["image_a"].build_args == ["--arg1", "val1", "--arg2=val2"]
    assert ctx.images["image_a"].env == {"SECRET_ENV": "secret:key"}
    assert ctx.images["image_a"].volumes == ["secret:key:/var/secret/key.txt"]
    assert ctx.images["image_a"].build_preset == "gpu-small"


async def test_project_level_defaults_live(
    assets: pathlib.Path, client: Client
) -> None:
    ws = assets / "with_project_yaml"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = LiveLocalCL(config_dir, client)
    try:
        flow = await RunningLiveFlow.create(cl, "live")
        job = await flow.get_job("test", {})
        assert "tag-a" in job.tags
        assert "tag-b" in job.tags
        assert job.env["global_a"] == "val-a"
        assert job.env["global_b"] == "val-b"
        assert job.env["global_b"] == "val-b"
        assert job.volumes == [
            "storage:common:/mnt/common:rw",
            "storage:dir:/var/dir:ro",
        ]
        assert job.workdir == RemotePath("/global/dir")
        assert job.life_span == 100800.0
        assert job.preset == "cpu-large"
        assert job.schedule_timeout == 2157741.0
        assert job.image == "image:banana"
    finally:
        await cl.close()


async def test_project_level_mixins_live(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "with_project_yaml"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = LiveLocalCL(config_dir, client)
    try:
        flow = await RunningLiveFlow.create(cl, "live")
        job = await flow.get_job("test_mixin", {})
        assert job.image == "mixin-image"
        assert job.preset == "mixin-preset"
    finally:
        await cl.close()


async def test_local_remote_path_images(
    client: Client, live_config_loader: ConfigLoader
) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-different-images")
    ctx = flow._ctx
    assert ctx.images.keys() == {"image_local", "image_remote"}

    assert ctx.images["image_local"].context == live_config_loader.workspace / "dir"
    assert (
        ctx.images["image_local"].dockerfile
        == live_config_loader.workspace / "dir/Dockerfile"
    )
    assert ctx.images["image_local"].dockerfile_rel == LocalPath("Dockerfile")

    assert ctx.images["image_remote"].context == URL(
        f"storage://{client.cluster_name}/{client.username}/dir"
    )
    assert ctx.images["image_remote"].dockerfile == URL(
        f"storage://{client.cluster_name}/{client.username}/dir/Dockerfile"
    )
    assert ctx.images["image_remote"].dockerfile_rel == RemotePath("Dockerfile")


async def test_defaults(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    ctx = flow._ctx
    assert ctx.tags == {"tag-a", "tag-b", "project:unit", "flow:live-full"}
    assert flow._defaults.workdir == RemotePath("/global/dir")
    assert flow._defaults.life_span == 100800.0
    assert flow._defaults.preset == "cpu-large"
    assert flow._defaults.schedule_timeout == 2157741.0


async def test_job(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-full")
    job = await flow.get_job("test_a", {})

    assert job.id == "test_a"
    assert job.title == "Job title"
    assert job.name == "job-name"
    assert job.image == "image:banana"
    assert job.preset == "cpu-micro"
    assert job.http_port == 8080
    assert not job.http_auth
    assert job.entrypoint == "bash"
    assert job.cmd == "echo abc"
    assert job.workdir == RemotePath("/local/dir")
    assert job.volumes == [
        "storage:common:/mnt/common:rw",
        "storage:dir:/var/dir:ro",
        "storage:dir:/var/dir:ro",
    ]
    assert job.tags == {
        "tag-1",
        "tag-2",
        "tag-a",
        "tag-b",
        "project:unit",
        "flow:live-full",
        "job:test-a",
    }
    assert job.life_span == 10500.0
    assert job.port_forward == ["2211:22"]
    assert job.detach
    assert job.browse


async def test_bad_expr_type_after_eval(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(
        live_config_loader, "live-bad-expr-type-after-eval"
    )

    with pytest.raises(EvalError) as cm:
        await flow.get_job("test", {})
    config_file = live_config_loader.workspace / "live-bad-expr-type-after-eval.yml"
    assert str(cm.value) == dedent(
        f"""\
        invalid literal for int() with base 10: 'abc def'
          in "{config_file}", line 6, column 20"""
    )


async def test_pipeline_minimal_ctx(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-minimal", "bake-id"
    )
    task = await flow.get_task((), "test_a", needs={}, state={})
    assert task.id == "test_a"
    assert task.title == "Batch title"
    assert task.name == "job-name"
    assert task.image == "image:banana"
    assert task.preset == "cpu-micro"
    assert task.http_port == 8080
    assert not task.http_auth
    assert task.entrypoint == "bash"
    assert task.cmd == "echo abc"
    assert task.workdir == RemotePath("/local/dir")
    assert task.volumes == [
        "storage:common:/mnt/common:rw",
        "storage:dir:/var/dir:ro",
        "storage:dir:/var/dir:ro",
    ]
    assert task.tags == {
        "tag-1",
        "tag-2",
        "tag-a",
        "tag-b",
        "task:test-a",
        "project:unit",
        "flow:batch-minimal",
        "bake_id:bake-id",
    }
    assert task.life_span == 10500.0
    assert task.strategy.max_parallel == 10
    assert task.strategy.fail_fast

    assert flow.graph == {"test_a": {}}


async def test_pipeline_seq(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-seq", "bake-id")

    task = await flow.get_task(
        (), "task-2", needs={"task-1": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )
    assert task.id is None
    assert task.title is None
    assert task.name is None
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.http_port is None
    assert not task.http_auth
    assert task.entrypoint is None
    assert task.cmd == "bash -euo pipefail -c 'echo def'"
    assert task.workdir is None
    assert task.volumes == []
    assert task.tags == {
        "project:unit",
        "flow:batch-seq",
        "task:task-2",
        "bake_id:bake-id",
        "bake_id:bake-id",
    }
    assert task.life_span is None
    assert task.strategy.max_parallel == 10
    assert task.strategy.fail_fast

    assert flow.graph == {"task-2": {"task-1": ast.NeedsLevel.COMPLETED}, "task-1": {}}


async def test_pipeline_needs(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-needs", "bake-id")

    task = await flow.get_task(
        (), "task-2", needs={"task_a": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )
    assert task.id is None
    assert task.title is None
    assert task.name is None
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.http_port is None
    assert not task.http_auth
    assert task.entrypoint is None
    assert task.cmd == "bash -euo pipefail -c 'echo def'"
    assert task.workdir is None
    assert task.volumes == []
    assert task.tags == {
        "project:unit",
        "flow:batch-needs",
        "task:task-2",
        "bake_id:bake-id",
    }
    assert task.life_span is None
    assert task.strategy.max_parallel == 10
    assert task.strategy.fail_fast

    assert flow.graph == {"task-2": {"task_a": ast.NeedsLevel.COMPLETED}, "task_a": {}}


async def test_pipeline_matrix(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-matrix", "bake-id")

    assert flow.graph == {
        "task-1-o3-t3": {},
        "task-1-o1-t1": {},
        "task-1-o2-t1": {},
        "task-1-o2-t2": {},
    }

    for task_id in flow.graph:
        task = await flow.get_task((), task_id, needs={}, state={})

        assert task.cache == CacheConf(
            strategy=ast.CacheStrategy.DEFAULT,
            life_span=1209600,
        )

        assert task.id is None
        assert task.title is None
        assert task.name is None
        assert task.image == "ubuntu"
        assert task.preset is None
        assert task.http_port is None
        assert not task.http_auth
        assert task.entrypoint is None
        assert task.cmd == "echo abc"
        assert task.workdir is None
        assert task.volumes == []
        assert task.tags == {
            "project:unit",
            "flow:batch-matrix",
            f"task:{task_id}",
            "bake_id:bake-id",
        }
        assert task.life_span is None
        assert task.strategy.max_parallel == 10
        assert task.strategy.fail_fast


async def test_matrix_dynamic(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-matrix-dynamic", "bake-id"
    )

    assert flow.graph == {
        "task-1-o1-t1": {},
        "task-1-o1-t2": {},
        "task-1-o2-t1": {},
        "task-1-o2-t2": {},
    }


async def test_pipeline_matrix_with_strategy(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-matrix-with-strategy", "bake-id"
    )

    assert flow.graph == {
        "task-1-o3-t3": {},
        "task-1-o1-t1": {},
        "task-1-o2-t1": {},
        "task-1-o2-t2": {},
        "simple": {
            "task-1-o3-t3": ast.NeedsLevel.COMPLETED,
            "task-1-o1-t1": ast.NeedsLevel.COMPLETED,
            "task-1-o2-t1": ast.NeedsLevel.COMPLETED,
            "task-1-o2-t2": ast.NeedsLevel.COMPLETED,
        },
    }

    task = await flow.get_task(
        (),
        "simple",
        needs={
            key: DepCtx(result=TaskStatus.SUCCEEDED, outputs={})
            for key in flow.graph["simple"]
        },
        state={},
    )
    assert task.strategy.max_parallel == 15
    assert task.strategy.fail_fast
    assert task.cache == CacheConf(
        strategy=ast.CacheStrategy.NONE,
        life_span=9000,
    )

    task = await flow.get_task((), "task-1-o3-t3", needs={}, state={})
    assert task.id is None
    assert task.title is None
    assert task.name is None
    assert task.image == "ubuntu"
    assert task.preset is None
    assert task.http_port is None
    assert not task.http_auth
    assert task.entrypoint is None
    assert task.cmd == "echo abc"
    assert task.workdir is None
    assert task.volumes == []
    assert task.tags == {
        "project:unit",
        "flow:batch-matrix-with-strategy",
        "task:task-1-o3-t3",
        "bake_id:bake-id",
    }
    assert task.life_span is None

    assert task.strategy.max_parallel == 5
    assert not task.strategy.fail_fast
    assert task.cache == CacheConf(
        strategy=ast.CacheStrategy.DEFAULT,
        life_span=5400,
    )


async def test_pipeline_matrix_2(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-matrix-with-deps", "bake-id"
    )

    assert flow.graph == {
        "task-2-a-1": {"task_a": ast.NeedsLevel.COMPLETED},
        "task-2-a-2": {"task_a": ast.NeedsLevel.COMPLETED},
        "task-2-b-1": {"task_a": ast.NeedsLevel.COMPLETED},
        "task-2-b-2": {"task_a": ast.NeedsLevel.COMPLETED},
        "task-2-c-1": {"task_a": ast.NeedsLevel.COMPLETED},
        "task-2-c-2": {"task_a": ast.NeedsLevel.COMPLETED},
        "task_a": {},
    }

    task = await flow.get_task((), "task_a", needs={}, state={})
    assert task.cache == CacheConf(
        strategy=ast.CacheStrategy.DEFAULT,
        life_span=1209600,
    )

    task = await flow.get_task(
        (),
        "task-2-a-1",
        needs={"task_a": DepCtx(TaskStatus.SUCCEEDED, {"name": "value"})},
        state={},
    )
    assert task.id is None
    assert task.title is None
    assert task.name is None
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.http_port is None
    assert not task.http_auth
    assert task.entrypoint is None
    assert task.cmd == ("""bash -euo pipefail -c \'echo "Task B a 1"\necho value\n\'""")
    assert task.workdir is None
    assert task.volumes == []
    assert task.tags == {
        "project:unit",
        "flow:batch-matrix-with-deps",
        "task:task-2-a-1",
        "bake_id:bake-id",
    }
    assert task.life_span is None

    assert task.cache == CacheConf(
        strategy=ast.CacheStrategy.DEFAULT,
        life_span=1209600,
    )


async def test_pipeline_matrix_with_doubles(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-matrix-doubles", "bake-id"
    )

    assert flow.graph == {
        "taskN0__0_1__0_3__0": {},
        "taskN1__0_1__0_5__1": {},
        "taskN2__0_2__0_3__2": {},
        "taskN3__0_2__0_5__3": {},
    }


async def test_pipeline_matrix_incomplete_include(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(
        EvalError,
        match=r"Keys of entry in include list of matrix "
        r"are not the same as matrix keys: missing keys: param2",
    ):
        await RunningBatchFlow.create(
            batch_config_loader, "batch-matrix-incomplete-include", "bake-id"
        )


async def test_pipeline_args_defautls_only(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-params", "bake-id")
    ctx = flow._ctx

    assert ctx.params == {"arg1": "val1", "arg2": "val2"}


async def test_pipeline_args_replaced(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-params", "bake-id", {"arg1": "new-val"}
    )
    ctx = flow._ctx

    assert ctx.params == {"arg1": "new-val", "arg2": "val2"}


async def test_pipeline_args_extra(batch_config_loader: ConfigLoader) -> None:
    with pytest.raises(ValueError, match=r"Unsupported arg\(s\): arg3"):
        await RunningBatchFlow.create(
            batch_config_loader, "batch-params", "bake-id", {"arg3": "new-val"}
        )


async def test_pipeline_args_missing_required(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(
        EvalError, match=r"Param arg2 is not initialized and has no default value"
    ):
        await RunningBatchFlow.create(
            batch_config_loader, "batch-params-required", "bake-id", {}
        )


async def test_pipeline_args_required_set(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-params-required", "bake-id", {"arg2": "val2"}
    )
    ctx = flow._ctx

    assert ctx.params == {"arg1": "val1", "arg2": "val2"}


async def test_batch_action_default(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-action-call", "bake-id"
    )
    flow2 = await flow.get_action("test", needs={})
    ctx = flow2._ctx
    assert ctx.inputs == {"arg1": "val 1", "arg2": "value 2"}
    task = await flow2.get_task((), "task_1", needs={}, state={})

    assert task.cache == CacheConf(strategy=ast.CacheStrategy.DEFAULT, life_span=1800)


def _make_ast_call(
    args: Mapping[str, Union[bool, int, float, str]]
) -> ast.BaseActionCall:
    def _make_simple_str_expr(res: Optional[str]) -> SimpleStrExpr:
        return SimpleStrExpr(
            Pos(0, 0, LocalPath("fake")), Pos(0, 0, LocalPath("fake")), res
        )

    def _make_primitive_expr(res: Union[bool, int, float, str]) -> PrimitiveExpr:
        return PrimitiveExpr(
            Pos(0, 0, LocalPath("fake")), Pos(0, 0, LocalPath("fake")), res
        )

    return ast.BaseActionCall(
        _start=Pos(0, 0, LocalPath("fake")),
        _end=Pos(0, 0, LocalPath("fake")),
        action=_make_simple_str_expr("ws:test"),
        args={key: _make_primitive_expr(value) for key, value in args.items()},
    )


def _make_ast_inputs(
    args: Mapping[str, Tuple[Optional[Union[bool, int, float, str]], InputType]]
) -> Mapping[str, ast.Input]:
    def _make_opt_primitive_expr(
        res: Optional[Union[bool, int, float, str]]
    ) -> SimpleOptPrimitiveExpr:
        return SimpleOptPrimitiveExpr(
            Pos(0, 0, LocalPath("fake")), Pos(0, 0, LocalPath("fake")), res
        )

    def _make_opt_str_expr(res: Optional[str]) -> SimpleOptStrExpr:
        return SimpleOptStrExpr(
            Pos(0, 0, LocalPath("fake")), Pos(0, 0, LocalPath("fake")), res
        )

    return {
        key: ast.Input(
            _start=Pos(0, 0, LocalPath("fake")),
            _end=Pos(0, 0, LocalPath("fake")),
            default=_make_opt_primitive_expr(value[0]),
            descr=_make_opt_str_expr(None),
            type=value[1],
        )
        for key, value in args.items()
    }


async def test_setup_inputs_ctx(
    batch_config_loader: ConfigLoader,
) -> None:

    with pytest.raises(EvalError, match=r"Required input\(s\): expected"):
        await setup_inputs_ctx(
            EMPTY_ROOT,
            _make_ast_call({"other": "1", "unknown": "2"}),
            _make_ast_inputs({"expected": (None, InputType.STR)}),
        )


async def test_batch_action_without_inputs_unsupported(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(EvalError, match=r"Unsupported input\(s\): other,unknown"):
        await setup_inputs_ctx(
            EMPTY_ROOT,
            _make_ast_call({"other": "1", "unknown": "2"}),
            _make_ast_inputs({}),
        )


async def test_batch_action_with_inputs_no_default(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(EvalError, match=r"Required input\(s\): arg1"):
        await setup_inputs_ctx(
            EMPTY_ROOT,
            _make_ast_call({"arg2": "2"}),
            _make_ast_inputs(
                {"arg1": (None, InputType.STR), "arg2": ("default", InputType.STR)}
            ),
        )


async def test_batch_action_with_inputs_ok(batch_config_loader: ConfigLoader) -> None:
    inputs = await setup_inputs_ctx(
        EMPTY_ROOT,
        _make_ast_call({"arg1": "v1", "arg2": "v2"}),
        _make_ast_inputs(
            {"arg1": (None, InputType.STR), "arg2": ("default", InputType.STR)}
        ),
    )

    assert inputs == {"arg1": "v1", "arg2": "v2"}


async def test_batch_action_with_inputs_default_ok(
    batch_config_loader: ConfigLoader,
) -> None:
    inputs = await setup_inputs_ctx(
        EMPTY_ROOT,
        _make_ast_call({"arg1": "v1"}),
        _make_ast_inputs(
            {"arg1": (None, InputType.STR), "arg2": ("default", InputType.STR)}
        ),
    )

    assert inputs == {"arg1": "v1", "arg2": "default"}


async def test_batch_action_with_inputs_types_do_not_match(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(
        EvalError,
        match=r"Type of argument 'arg1' do not match to with inputs"
        r" declared type. Argument has type 'str', declared "
        r"input type is 'bool'",
    ):
        await setup_inputs_ctx(
            EMPTY_ROOT,
            _make_ast_call({"arg1": "v1"}),
            _make_ast_inputs(
                {"arg1": (None, InputType.BOOL), "arg2": ("default", InputType.STR)}
            ),
        )


async def test_local_call_with_cache_invalid(
    assets: pathlib.Path,
    client: Client,
) -> None:
    config_dir = ConfigDir(
        workspace=assets / "local_actions",
        config_dir=assets / "local_actions",
    )
    cl = BatchLocalCL(config_dir, client)

    with pytest.raises(
        EvalError,
        match=r"Specifying cache in action call to the action "
        r"ws:cp of kind local is not supported.",
    ):
        await RunningBatchFlow.create(cl, "bad-call-with-cache", "bake-id", {})


async def test_stateful_call_with_cache_invalid(
    assets: pathlib.Path,
    client: Client,
) -> None:
    config_dir = ConfigDir(
        workspace=assets / "stateful_actions",
        config_dir=assets / "stateful_actions",
    )
    cl = BatchLocalCL(config_dir, client)

    with pytest.raises(
        EvalError,
        match=r"Specifying cache in action call to the action "
        r"ws:with-state of kind stateful is not supported.",
    ):
        await RunningBatchFlow.create(cl, "bad-call-with-cache", "bake-id", {})


async def test_job_with_live_action(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-action-call")
    job = await flow.get_job("test", {})

    assert job.id == "test"
    assert job.title == "live_action_call.test"
    assert job.name is None
    assert job.image == "ubuntu"
    assert job.preset is None
    assert job.http_port is None
    assert not job.http_auth
    assert job.entrypoint is None
    assert job.cmd == "bash -euo pipefail -c 'echo A val 1 B 2 C'"
    assert job.workdir is None
    assert job.volumes == []
    assert job.tags == {
        "project:unit",
        "flow:live-action-call",
        "job:test",
    }
    assert job.life_span is None
    assert job.port_forward == []
    assert not job.detach
    assert not job.browse


async def test_job_with_live_module(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-module-call")
    job = await flow.get_job("test", {})

    assert job.id == "test"
    assert job.title == "live_module_call.test"
    assert job.name is None
    assert job.image == "ubuntu"
    assert job.preset == "test-preset"
    assert job.http_port is None
    assert not job.http_auth
    assert job.entrypoint is None
    assert job.cmd == "bash -euo pipefail -c 'echo A val 1 B live_module_call C'"
    assert job.workdir == pathlib.PurePosixPath("/some/dir")
    assert job.volumes == ["storage:test:/volume"]
    assert job.tags == {
        "project:unit",
        "flow:live-module-call",
        "job:test",
        "test-tag",
    }
    assert job.env == {"TEST": "test_value"}
    assert job.life_span == timedelta(days=2).total_seconds()
    assert job.schedule_timeout == timedelta(minutes=60).total_seconds()
    assert job.port_forward == []
    assert not job.detach
    assert not job.browse


async def test_job_with_live_call_to_remote_module_invalid(
    live_config_loader: ConfigLoader,
) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-module-remote-call")
    with pytest.raises(
        EvalError,
        match=r"Module call to non local action 'gh:username/repo@tag' is forbidden",
    ):
        await flow.get_job("test", {})


async def test_job_with_mixins(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-mixins")
    job = await flow.get_job("test", {})

    assert job.id == "test"
    assert job.image == "ubuntu"
    assert job.preset == "cpu-micro"
    assert job.env == {
        "env1": "val1",
        "env2": "val2",
        "env3": "val-mixin2-3",
        "env4": "val-mixin2-4",
    }

    job = await flow.get_job("test2", {})

    assert job.id == "test2"
    assert job.image == "ubuntu2"

    job = await flow.get_job("test3", {})

    assert job.id == "test3"
    assert job.image == "ubuntu"
    assert job.volumes == ["storage:dir2:/var/dir2:ro", "storage:dir1:/var/dir1:ro"]

    job = await flow.get_job("test4", {"test_expr": "test_name"})

    assert job.id == "test4"
    assert job.image == "ubuntu"
    assert job.name == "test_name"


async def test_job_with_sub_mixins(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-sub-mixins")
    job = await flow.get_job("test", {})

    assert job.id == "test"
    assert job.image == "ubuntu"
    assert job.env == {
        "env1": "val-mixin1-1",
        "env2": "val-mixin2-2",
        "env3": "val-mixin2-3",
    }


async def test_job_with_params(live_config_loader: ConfigLoader) -> None:
    flow = await RunningLiveFlow.create(live_config_loader, "live-params")
    job = await flow.get_job("test", {"arg1": "value"})

    assert job.id == "test"
    assert job.title == "live_params.test"
    assert job.name is None
    assert job.image == "ubuntu"
    assert job.preset is None
    assert job.http_port is None
    assert not job.http_auth
    assert job.entrypoint is None
    assert job.cmd == "bash -euo pipefail -c 'echo value val2 live_params'"
    assert job.workdir is None
    assert job.volumes == []
    assert job.tags == {
        "project:unit",
        "flow:live-params",
        "job:test",
    }
    assert job.life_span is None
    assert job.port_forward == []
    assert not job.detach
    assert not job.browse


async def test_pipeline_enable_default_no_needs(
    batch_config_loader: ConfigLoader,
) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-enable", "bake-id")
    meta = await flow.get_meta("task_a", needs={}, state={})

    assert meta.enable


async def test_pipeline_enable_default_with_needs(
    batch_config_loader: ConfigLoader,
) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-needs", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.FAILED, {})}, state={}
    )

    assert not meta.enable

    flow = await RunningBatchFlow.create(batch_config_loader, "batch-needs", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.SKIPPED, {})}, state={}
    )

    assert not meta.enable

    flow = await RunningBatchFlow.create(batch_config_loader, "batch-needs", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )

    assert meta.enable


async def test_pipeline_enable_success(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-enable", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.FAILED, {})}, state={}
    )

    assert not meta.enable

    flow = await RunningBatchFlow.create(batch_config_loader, "batch-enable", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.SKIPPED, {})}, state={}
    )

    assert not meta.enable

    flow = await RunningBatchFlow.create(batch_config_loader, "batch-enable", "bake-id")
    meta = await flow.get_meta(
        "task-2", needs={"task_a": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )

    assert meta.enable


async def test_pipeline_with_batch_action(batch_config_loader: ConfigLoader) -> None:

    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-action-call", "bake-id"
    )

    assert await flow.is_action("test")
    flow2 = await flow.get_action("test", needs={})

    task = await flow2.get_task(("test",), "task_1", needs={}, state={})
    assert task.id == "task_1"
    assert task.title is None
    assert task.name is None
    assert task.image == "ubuntu"
    assert task.preset is None
    assert task.http_port is None
    assert not task.http_auth
    assert task.entrypoint is None
    assert (
        task.cmd == "bash -euo pipefail -c 'echo ::set-output name=task1::Task 1 val 1'"
    )
    assert task.workdir is None
    assert task.volumes == []
    assert task.tags == {
        "project:unit",
        "flow:batch-action-call",
        "task:test.task-1",
        "bake_id:bake-id",
    }
    assert task.life_span is None
    assert task.strategy.max_parallel == 10
    assert task.strategy.fail_fast

    assert flow2.graph == {
        "task_1": {},
        "task_2": {"task_1": ast.NeedsLevel.COMPLETED},
    }


async def test_wrong_needs(
    batch_config_loader: ConfigLoader,
) -> None:
    with pytest.raises(
        EvalError,
        match=r"Task task-2 needs unknown task something_wrong.*",
    ):
        await RunningBatchFlow.create(
            batch_config_loader, "batch-wrong-need", "bake-id"
        )


async def test_pipeline_life_span(
    batch_config_loader: ConfigLoader,
) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-life-span", "bake-id"
    )
    assert flow.life_span == timedelta(days=30)


async def test_early_images(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "batch_images"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch", "bake-id")
        assert flow.early_images["image1"].ref == "image:main"
        assert flow.early_images["image1"].context == ws / "dir"
        assert flow.early_images["image1"].dockerfile == ws / "dir/Dockerfile"

        action = await flow.get_action_early("action")

        assert action.early_images["image_early"].ref == "image:banana1"
        assert action.early_images["image_early"].context == ws / "dir"
        assert action.early_images["image_early"].dockerfile == ws / "dir/Dockerfile"

        assert action.early_images["image_late"].ref == "image:banana2"
        assert action.early_images["image_late"].context is None
        assert action.early_images["image_late"].dockerfile is None
    finally:
        await cl.close()


def test_sanitize_name() -> None:
    assert sanitize_name("myproject") == "myproject"
    assert sanitize_name("проект") == "проект"
    assert sanitize_name("my project") == "my_project"
    assert sanitize_name("my:project") == "my_project"
    assert sanitize_name("my/project") == "my/project"
    assert sanitize_name("my//project") == "my/project"
    assert sanitize_name("/my/project/") == "my/project"
    assert sanitize_name("") == "_"


async def test_batch_module_call_to_remote_invalid(
    assets: pathlib.Path, client: Client
) -> None:
    ws = assets / "batch_module"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        with pytest.raises(
            EvalError,
            match=r"Module call to non local action 'gh:username/repo@tag' "
            r"is forbidden",
        ):
            await RunningBatchFlow.create(cl, "batch-module-remote-call", "bake-id")
    finally:
        await cl.close()


async def test_batch_with_mixins(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(batch_config_loader, "batch-mixin", "bake-id")
    task = await flow.get_task((), "task-1", needs={}, state={})

    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "bash -euo pipefail -c 'echo abc'"

    task = await flow.get_task(
        (), "task-2", needs={"task-1": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "bash -euo pipefail -c 'echo def'"


async def test_batch_with_mixins_with_bash_python_properties(
    batch_config_loader: ConfigLoader,
) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-mixin-with-bash-python-properties", "bake-id"
    )
    task = await flow.get_task((), "task-1", needs={}, state={})

    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "bash -euo pipefail -c 'echo abc'"

    task = await flow.get_task(
        (), "task-2", needs={"task-1": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "python3 -uc 'print(\"abc\")'"


async def test_batch_with_sub_mixins(batch_config_loader: ConfigLoader) -> None:
    flow = await RunningBatchFlow.create(
        batch_config_loader, "batch-sub-mixin", "bake-id"
    )
    task = await flow.get_task((), "task-1", needs={}, state={})

    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "bash -euo pipefail -c 'echo abc'"
    assert task.env == {
        "env1": "val-mixin1-1",
        "env2": "val-mixin1-2",
    }

    task = await flow.get_task(
        (), "task-2", needs={"task-1": DepCtx(TaskStatus.SUCCEEDED, {})}, state={}
    )
    assert task.image == "ubuntu"
    assert task.preset == "cpu-micro"
    assert task.cmd == "bash -euo pipefail -c 'echo def'"
    assert task.env == {
        "env1": "val-mixin1-1",
        "env2": "val-mixin2-2",
        "env3": "val-mixin2-3",
    }


async def test_batch_module_with_mixin(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "batch_mixins"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch-module-call", "bake-id")
        module_flow = await flow.get_action("test", needs={})
        task = await module_flow.get_task(("test",), "task_1", needs={}, state={})

        assert task.image == "ubuntu"
        assert task.preset == "cpu-micro"
        assert task.cmd == "bash -euo pipefail -c 'echo abc'"
    finally:
        await cl.close()


async def test_batch_action_no_access_to_mixin(
    assets: pathlib.Path, client: Client
) -> None:
    ws = assets / "batch_mixins"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch-action-call", "bake-id")
        with pytest.raises(
            EvalError,
            match=r"Unknown mixin 'basic'",
        ):
            await flow.get_action("test", needs={})

    finally:
        await cl.close()


async def test_batch_task_with_no_image(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "batch_mixins"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        with pytest.raises(
            EvalError,
            match=r"Image for task test is not specified",
        ):
            await RunningBatchFlow.create(cl, "batch-task-no-image", "bake-id")

    finally:
        await cl.close()


async def test_early_images_include_globals(
    assets: pathlib.Path, client: Client
) -> None:
    ws = assets / "with_project_yaml"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch", "bake-id")
        assert flow.early_images["image_a"].ref == "image:banana"
        assert flow.early_images["image_a"].context == ws / "dir"
        assert flow.early_images["image_a"].dockerfile == ws / "dir/Dockerfile"

        assert flow.early_images["image_b"].ref == "image:main"
        assert flow.early_images["image_b"].context == ws / "dir"
        assert flow.early_images["image_b"].dockerfile == ws / "dir/Dockerfile"

    finally:
        await cl.close()


async def test_batch_with_project_globals(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "with_project_yaml"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch", "bake-id")
        task = await flow.get_task((), "task", needs={}, state={})
        assert "tag-a" in task.tags
        assert "tag-b" in task.tags
        assert task.env["global_a"] == "val-a"
        assert task.env["global_b"] == "val-b"
        assert task.volumes == [
            "storage:common:/mnt/common:rw",
            "storage:dir:/var/dir:ro",
        ]
        assert task.workdir == RemotePath("/global/dir")
        assert task.life_span == 100800.0
        assert task.preset == "cpu-large"
        assert task.schedule_timeout == 2157741.0
        assert task.image == "image:main"

        assert not task.strategy.fail_fast
        assert task.strategy.max_parallel == 20
        assert task.cache.strategy == CacheStrategy.NONE
        assert task.cache.life_span == 9000.0

    finally:
        await cl.close()


async def test_batch_with_project_mixins(assets: pathlib.Path, client: Client) -> None:
    ws = assets / "with_project_yaml"
    config_dir = ConfigDir(
        workspace=ws,
        config_dir=ws,
    )
    cl = BatchLocalCL(config_dir, client)
    try:
        flow = await RunningBatchFlow.create(cl, "batch", "bake-id")
        task = await flow.get_task((), "test_mixin", needs={}, state={})
        assert task.image == "mixin-image"
        assert task.preset == "mixin-preset"

        task = await flow.get_task((), "test_mixin_cmd", needs={}, state={})
        assert task.image == "mixin-image"
        assert task.cmd == "command -o --option arg1 arg2"

        task = await flow.get_task((), "test_mixin_bash", needs={}, state={})
        assert task.image == "mixin-image"
        assert task.cmd == (
            "bash -euo pipefail -c 'command -o --option arg1 arg2\n"
            "command2 -o --option arg1 arg2\n'"
        )

        task = await flow.get_task((), "test_mixin_python", needs={}, state={})
        assert task.image == "mixin-image"
        assert task.cmd == "python3 -uc 'print(\"hello neuro-flow\")\n'"

    finally:
        await cl.close()
