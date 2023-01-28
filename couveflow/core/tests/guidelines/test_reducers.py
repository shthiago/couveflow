import pytest

from couveflow.core.guidelines.reducers import (ArithmeticReducer,
                                                LogicalReducer,
                                                RelationalReducer)
from couveflow.core.guidelines.structures import (ArithmeticOperator,
                                                  ArithmeticSequence,
                                                  LogicalOperator,
                                                  LogicalSequence, Operand,
                                                  RelationalOperator)


class TestArithmeticReducer:
    @pytest.mark.parametrize(
        ("base", "sequence", "expected_result"),
        [
            (
                12,
                [(ArithmeticOperator.SUM, 12)],
                24,
            ),
            (
                12,
                [
                    (ArithmeticOperator.SUM, 12),
                    (ArithmeticOperator.SUM, 12),
                ],
                36,
            ),
            (
                12,
                [(ArithmeticOperator.SUB, 12)],
                0,
            ),
            (
                12,
                [
                    (ArithmeticOperator.SUB, 12),
                    (ArithmeticOperator.SUB, 12),
                ],
                -12,
            ),
            (
                12,
                [
                    (ArithmeticOperator.SUM, 12),
                    (ArithmeticOperator.SUB, 12),
                ],
                12,
            ),
        ]
    )
    def test_reduce(self, base: Operand, sequence: ArithmeticSequence, expected_result: Operand):
        assert ArithmeticReducer.reduce(base, sequence) == expected_result

    def test_failure(self):
        with pytest.raises(ValueError):
            ArithmeticReducer.reduce(12, [(12, "truly invalid operator")])


class TestRelationalReducer:
    @pytest.mark.parametrize(
        ("first", "operator", "second", "expected_result"),
        [
            (
                12,
                RelationalOperator.EQ,
                24,
                False,
            ),
            (
                12,
                RelationalOperator.DIFF,
                24,
                True,
            ),
            (
                12,
                RelationalOperator.LT,
                24,
                True,
            ),
            (
                24,
                RelationalOperator.LT,
                12,
                False,
            ),
            (
                12,
                RelationalOperator.LTE,
                24,
                True,
            ),
            (
                24,
                RelationalOperator.LTE,
                24,
                True,
            ),
            (
                24,
                RelationalOperator.LTE,
                12,
                False,
            ),
            (
                24,
                RelationalOperator.GT,
                12,
                True,
            ),
            (
                12,
                RelationalOperator.GT,
                24,
                False,
            ),
            (
                24,
                RelationalOperator.GTE,
                12,
                True,
            ),
            (
                24,
                RelationalOperator.GTE,
                24,
                True,
            ),
            (
                12,
                RelationalOperator.GTE,
                24,
                False,
            ),
        ]
    )
    def test_reduce(
        self,
        first: Operand,
        operator: RelationalOperator,
        second: Operand,
        expected_result: bool
    ):
        assert RelationalReducer.reduce(
            first, operator, second) == expected_result

    def test_failure(self):
        with pytest.raises(ValueError):
            RelationalReducer.reduce(12, "truly invalid operator", "a")


class TestLogicalReducer:
    @pytest.mark.parametrize(
        ("base", "sequence", "expected_result"),
        [
            (
                True,
                [(LogicalOperator.AND, False)],
                False,
            ),
            (
                True,
                [(LogicalOperator.AND, True)],
                True,
            ),
            (
                False,
                [(LogicalOperator.AND, True)],
                False,
            ),
            (
                False,
                [(LogicalOperator.AND, False)],
                False,
            ),
            (
                True,
                [(LogicalOperator.OR, False)],
                True,
            ),
            (
                True,
                [(LogicalOperator.OR, True)],
                True,
            ),
            (
                False,
                [(LogicalOperator.OR, True)],
                True,
            ),
            (
                False,
                [(LogicalOperator.OR, False)],
                False,
            ),
        ]
    )
    def test_reduce(self, base: bool, sequence: LogicalSequence, expected_result: bool):
        assert LogicalReducer.reduce(base, sequence) == expected_result

    def test_failure(self):
        with pytest.raises(ValueError):
            LogicalReducer.reduce(12, [(12, "truly invalid operator")])
