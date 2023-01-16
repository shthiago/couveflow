from typing import List

import pytest

from couveflow.core.guidelines.lexer import GuidelineLexer


class TestLexer:
    @pytest.mark.parametrize(
        ("expression", "token_types"),
        [
            (
                "last_interaction_timestamp('my_id')",
                [
                    "FUNCTION",
                    "L_PARENTESIS",
                    "STRING",
                    "R_PARENTESIS",
                ]
            ),
            (
                "15 > 12",
                [
                    "INTEGER",
                    "LOG_GREATER_THAN",
                    "INTEGER",
                ]
            ),
            (
                "last_measure_for('my_id', 'sensorA') > 12",
                [
                    "FUNCTION",
                    "L_PARENTESIS",
                    "STRING",
                    "COMMA",
                    "STRING",
                    "R_PARENTESIS",
                    "LOG_GREATER_THAN",
                    "INTEGER",
                ]
            ),
            (
                "12.1 <= 12.3",
                [
                    "FLOAT",
                    "LOG_LESS_THAN_EQUAL",
                    "FLOAT",
                ]
            ),
        ]
    )
    def test_identify_tokens(self, expression: str, token_types: List[str]):
        lexer = GuidelineLexer()
        lexer.input(expression)

        for type in token_types:
            token = lexer.token()
            assert token.type == type
