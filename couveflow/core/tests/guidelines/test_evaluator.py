from typing import Union
import pytest

from couveflow.core.guidelines.evaluator import GuidelineEvaluator
from couveflow.core.tests.factories import VariableFactory


@pytest.mark.django_db
class TestGuidelineEvaluator:
    @pytest.mark.parametrize(
        ('expression', 'expected_result'),
        [
            (
                '',
                True
            ),
            (
                '0',
                False
            ),
            (
                '12 > 11',
                True
            ),
            (
                '12.1 > 11.2',
                True
            ),
            (
                '12.1 > 12',
                True
            ),
            (
                '12.1 > 12.2',
                False
            ),
            (
                '12 < 11',
                False
            ),
            (
                '12 > 11 + 2',
                False
            ),
            (
                '12 < 11 + 2',
                True
            ),
            (
                '12 + 1 <= 11 + 2',
                True
            ),
            (
                '12 + 1 >= 11 + 2',
                True
            ),
            (
                '12 + 1 >= 11 + 2',
                True
            ),
            (
                '12 + 1 <= 11',
                False
            ),
        ],
    )
    def test_evaluator_basic_expressions(self, expression: str, expected_result: bool):
        evaluator = GuidelineEvaluator()
        value = evaluator.evaluate(expression)

        assert value == expected_result

    @pytest.mark.parametrize(
        ('var_name', 'var_value', 'expression', 'expected_result'),
        [
            (
                'foo',
                10,
                "var('foo') > 9",
                True,
            ),
            (
                'foo',
                8,
                "var('foo') > 9",
                False,
            ),
            (
                'foo',
                'a',
                "var('foo') > 'b'",
                True,
            ),
            (
                'foo',
                'a',
                "var('foo') < 'b'",
                False,
            ),
        ],
    )
    def test_evaluator_variable(self, var_name: str, var_value: Union[str, int, float], expression: str, expected_result: bool):
        VariableFactory(name=var_name, value=var_value)
        evaluator = GuidelineEvaluator()
        value = evaluator.evaluate(expression)

        assert value == expected_result
