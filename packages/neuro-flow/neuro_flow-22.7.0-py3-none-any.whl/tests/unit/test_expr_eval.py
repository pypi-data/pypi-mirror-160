import pytest
from contextlib import asynccontextmanager
from neuro_sdk import Client
from typing import Any, AsyncIterator, Dict, List
from typing_extensions import Final

from neuro_flow.context import DepCtx
from neuro_flow.expr import (
    PARSER,
    EvalError,
    FloatExpr,
    MappingExpr,
    RootABC,
    SequenceExpr,
    StrExpr,
    TypeT,
)
from neuro_flow.tokenizer import Pos, tokenize
from neuro_flow.types import LocalPath, TaskStatus


FNAME = LocalPath("<test>")
START: Final = Pos(0, 0, FNAME)


class DictContext(RootABC):
    def __init__(
        self, dct: Dict[str, TypeT], client: Client, dry_run: bool = False
    ) -> None:
        self._dct = dct
        self._client = client
        self._dry_run = dry_run

    def lookup(self, name: str) -> TypeT:
        return self._dct[name]

    @asynccontextmanager
    async def client(self) -> AsyncIterator[Client]:
        yield self._client

    @property
    def dry_run(self) -> bool:
        return self._dry_run


@pytest.mark.parametrize(
    "expr,context,result",
    [
        ("((((True))))", {}, True),  # Can be very slow with poor parser
        ('"foo" == "foo"', {}, True),
        ('"foo" == "bar"', {}, False),
        ("4 < 5", {}, True),
        ("4 > 5", {}, False),
        ("(4 > 5) or ((4 <= 5))", {}, True),
        ("len(foo) <= 5", {"foo": [1, 2, 3]}, True),
        ("len(foo) >= 5", {"foo": [1, 2, 3]}, False),
        ("(2 == 3) or True", {}, True),
        ("'sdfdsf' == True", {}, False),
        ("not True", {}, False),
        ("not (42 == 42) or not True", {}, False),
        ("-2 < 4 and 7 < 6", {}, False),
        ("-2 < -4 or 7 < 6 ", {}, False),
        ("1 < -2 or 2 < 4 ", {}, True),
    ],
)
async def test_bool_evals(
    expr: str, context: Dict[str, TypeT], result: bool, client: Client
) -> None:
    parsed = PARSER.parse(list(tokenize("${{" + expr + "}}", START)))
    assert len(parsed) == 1
    assert result == await parsed[0].eval(DictContext(context, client))


@pytest.mark.parametrize(
    "expr,context,result",
    [
        ("4 * 5 + 2", {}, 22),
        ("0 * 5 + 2 / 2", {}, 1),
        ("0 * (2 / 2 + 1)", {}, 0),
        ("2 * 6 / 12 + 5 - 2 ", {}, 4),
    ],
)
async def test_arithmetic_evals(
    expr: str, context: Dict[str, TypeT], result: int, client: Client
) -> None:
    parsed = PARSER.parse(list(tokenize("${{" + expr + "}}", START)))
    assert len(parsed) == 1
    assert result == await parsed[0].eval(DictContext(context, client))


@pytest.mark.parametrize(
    "expr,statuses,result",
    [
        ("success()", [], True),
        ("success()", [TaskStatus.SUCCEEDED], True),
        ("success()", [TaskStatus.SUCCEEDED, TaskStatus.SUCCEEDED], True),
        ("success()", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], False),
        ("success()", [TaskStatus.SUCCEEDED, TaskStatus.SKIPPED], False),
        ("success('task_1')", [TaskStatus.SUCCEEDED], True),
        (
            "success('task_1', 'task_2')",
            [TaskStatus.SUCCEEDED, TaskStatus.SUCCEEDED],
            True,
        ),
        ("success('task_1')", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], True),
        ("success('task_2')", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], False),
        ("success('task_2')", [TaskStatus.SUCCEEDED, TaskStatus.SKIPPED], False),
    ],
)
async def test_success_func(
    expr: str, statuses: List[TaskStatus], result: bool, client: Client
) -> None:
    context = {
        "needs": {
            f"task_{num}": DepCtx(status, {}) for num, status in enumerate(statuses, 1)
        }
    }
    parsed = PARSER.parse(list(tokenize("${{" + expr + "}}", START)))
    assert len(parsed) == 1
    assert result == await parsed[0].eval(DictContext(context, client))  # type: ignore


@pytest.mark.parametrize(
    "expr,statuses,result",
    [
        ("failure()", [], False),
        ("failure()", [TaskStatus.SUCCEEDED], False),
        ("failure()", [TaskStatus.SUCCEEDED, TaskStatus.SUCCEEDED], False),
        ("failure()", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], True),
        ("failure()", [TaskStatus.SUCCEEDED, TaskStatus.SKIPPED], False),
        ("failure('task_1')", [TaskStatus.SUCCEEDED], False),
        (
            "failure('task_1', 'task_2')",
            [TaskStatus.SUCCEEDED, TaskStatus.SUCCEEDED],
            False,
        ),
        (
            "failure('task_1', 'task_2')",
            [TaskStatus.SUCCEEDED, TaskStatus.FAILED],
            True,
        ),
        ("failure('task_1')", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], False),
        ("failure('task_2')", [TaskStatus.SUCCEEDED, TaskStatus.FAILED], True),
        ("failure('task_2')", [TaskStatus.SUCCEEDED, TaskStatus.SKIPPED], False),
        ("failure('task_1', 'task_2')", [TaskStatus.FAILED, TaskStatus.SKIPPED], True),
    ],
)
async def test_failure_func(
    expr: str, statuses: List[TaskStatus], result: bool, client: Client
) -> None:
    context = {
        "needs": {
            f"task_{num}": DepCtx(status, {}) for num, status in enumerate(statuses, 1)
        }
    }
    parsed = PARSER.parse(list(tokenize("${{" + expr + "}}", START)))
    assert len(parsed) == 1
    assert result == await parsed[0].eval(DictContext(context, client))  # type: ignore


def test_parse_empty_float() -> None:
    with pytest.raises(EvalError):
        FloatExpr(START, START, "")


def test_parse_implicit_concatenation_of_float() -> None:
    with pytest.raises(EvalError):
        pat = "${{ 1 }}_${{ 2 }}"
        FloatExpr(START, Pos(0, len(pat), FNAME), pat)


async def test_concat_str(client: Client) -> None:
    pat = "${{ 'a' + 'b' }}"
    expr = StrExpr(START, Pos(0, len(pat), FNAME), pat)
    assert "ab" == await expr.eval(DictContext({}, client))


async def test_add_float(client: Client) -> None:
    pat = "${{ 1 + 2 }}"
    expr = FloatExpr(START, Pos(0, len(pat), FNAME), pat)
    assert 3 == await expr.eval(DictContext({}, client))


async def test_sub_float(client: Client) -> None:
    pat = "${{ 3 - 2 }}"
    expr = FloatExpr(START, Pos(0, len(pat), FNAME), pat)
    assert 1 == await expr.eval(DictContext({}, client))


async def test_mul_float(client: Client) -> None:
    pat = "${{ 2 * 3 }}"
    expr = FloatExpr(START, Pos(0, len(pat), FNAME), pat)
    assert 6 == await expr.eval(DictContext({}, client))


async def test_div_float(client: Client) -> None:
    pat = "${{ 1 / 2 }}"
    expr = FloatExpr(START, Pos(0, len(pat), FNAME), pat)
    assert 0.5 == await expr.eval(DictContext({}, client))


async def test_concat_list(client: Client) -> None:
    pat = "${{ [1] + [2] }}"
    expr = SequenceExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert [1, 2] == await expr.eval(DictContext({}, client))  # type: ignore


async def test_concat_empty_list(client: Client) -> None:
    pat = "${{ [1] + [] }}"
    expr = SequenceExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert [1] == await expr.eval(DictContext({}, client))  # type: ignore


async def test_concat_dict(client: Client) -> None:
    pat = "${{ {'a': 1} | {'b': 2} }}"
    expr = MappingExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert {"a": 1, "b": 2} == await expr.eval(DictContext({}, client))  # type: ignore


async def test_concat_empty_dict(client: Client) -> None:
    pat = "${{ {'a': 1} | {} }}"
    expr = MappingExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert {"a": 1} == await expr.eval(DictContext({}, client))  # type: ignore


async def test_list_trailing_comm(client: Client) -> None:
    pat = "${{ [1,2,] }}"
    expr = SequenceExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert [1, 2] == await expr.eval(DictContext({}, client))  # type: ignore


async def test_dict_trailing_comma(client: Client) -> None:
    pat = "${{ {'a': 1, 'b': 2,} }}"
    expr = MappingExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert {"a": 1, "b": 2} == await expr.eval(DictContext({}, client))  # type: ignore


@pytest.mark.parametrize(
    "expr,context,result",
    [
        ("2 if True else 3", {}, 2),
        ("2 if False else 3", {}, 3),
        ("2 if True else 0 / 0", {}, 2),
        ("0 / 0 if False else 2", {}, 2),
        ("0 / 0 if False else 2", {}, 2),
        (
            "2 if some_ctx else 3",
            {
                "some_ctx": True,
            },
            2,
        ),
        ("2 if (3 if (4 if False else False) else False) else 3", {}, 3),
    ],
)
async def test_if_else_expr(
    client: Client, expr: str, context: Dict[str, Any], result: Any
) -> None:
    parsed = PARSER.parse(list(tokenize("${{" + expr + "}}", START)))
    assert len(parsed) == 1
    assert result == await parsed[0].eval(DictContext(context, client))


async def test_list_comp(client: Client) -> None:
    pat = "${{ [x * x for x in range(5)] }}"
    expr = SequenceExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert [0, 1, 4, 9, 16] == await expr.eval(DictContext({}, client))  # type: ignore


async def test_list_comp_with_if(client: Client) -> None:
    pat = "${{ [x * x for x in range(5) if x % 2 == 0] }}"
    expr = SequenceExpr(START, Pos(0, len(pat), FNAME), pat, int)  # type: ignore
    assert [0, 4, 16] == await expr.eval(DictContext({}, client))  # type: ignore
