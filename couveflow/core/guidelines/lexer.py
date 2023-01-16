from typing import Optional

from ply import lex

from couveflow.core.guidelines.functions import FUNCTIONS


class GuidelineLexer:
    def __init__(self):
        self._lexer = lex.lex(module=self)

    def input(self, *args, **kwargs):
        self._lexer.input(*args, **kwargs)

    def token(self, *args, **kwargs) -> Optional[lex.LexToken]:
        return self._lexer.token()

    tokens = (
        'FUNCTION',
        'VARIABLE',
        'LOG_OR',
        'LOG_AND',
        'LOG_GREATER_THAN',
        'LOG_GREATER_THAN_EQUAL',
        'LOG_LESS_THAN',
        'LOG_LESS_THAN_EQUAL',
        'LOG_EQUAL_TO',
        'ARIT_PLUS',
        'ARIT_MINUS',
        'L_PARENTESIS',
        'R_PARENTESIS',
        'COMMA',
        'FLOAT',
        'INTEGER',
        'STRING',
    )

    t_STRING = r'\'\w+\''
    t_VARIABLE = r'var'
    t_LOG_OR = r'or'
    t_LOG_AND = r'and'
    t_LOG_GREATER_THAN = r'>'
    t_LOG_GREATER_THAN_EQUAL = r'>='
    t_LOG_LESS_THAN = r'<'
    t_LOG_LESS_THAN_EQUAL = r'<='
    t_LOG_EQUAL_TO = r'=='
    t_ARIT_PLUS = r'\+'
    t_ARIT_MINUS = r'-'
    t_L_PARENTESIS = r'\('
    t_R_PARENTESIS = r'\)'
    t_COMMA = r','

    def t_FLOAT(self, token: lex.LexToken):
        r'\d*\.\d+'
        token.value = float(token.value)

        return token

    def t_INTEGER(self, token: lex.LexToken):
        r'\d+(?!\.)'
        token.value = int(token.value)

        return token

    def t_FUNCTION(self, token: lex.LexToken):
        r'[A-Za-z]\w+'
        if token.value == 'var':
            token.type = 'VARIABLE'
            return token
        
        if token.value not in FUNCTIONS.keys():
            raise ValueError(f'Invalid function: {token.value}')

        return token

    t_ignore = ' \t\n'

    def t_error(self, token: lex.LexToken):
        print("Illegal character '%s'" % token.value[0])
        token.lexer.skip(1)
