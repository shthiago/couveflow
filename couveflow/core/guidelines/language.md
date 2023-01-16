# Productions

Expression ::= LogicalExpression | &

LogicalExpression ::= ArithmeticExpression LogicalExpressionAux
LogicalExpressionAux ::= LogicalOperator LogicalExpression LogicalExpressionAux | &

LogicalOperator ::= LOG_OR | LOG_AND | LOG_GREATER_THAN | LOG_GREATER_THAN_EQUAL | LOG_LESS_THAN | LOG_LESS_THAN_EQUAL

ArithmeticExpression ::= Operand ArithmeticExpressionAux
ArithmeticExpressionAux ::= ArithmeticOperator ArithmeticExpressionAux | &

ArithmeticOperator ::= ARIT_PLUS | ARIT_MINUS

Operand ::= NativeOperand | FuncCall | Variable

NativeOperand ::= INTEGER | FLOAT | STRING

FuncCall ::= FUNCTION L_PARENTESIS Parameters R_PARENTESIS

Variable ::= VARIABLE L_PARENTESIS STRING R_PARENTESIS

Parameters ::= NativeOperand MoreParameters
Parameters ::= FuncCall MoreParameters

MoreParameters ::= COMMA Parameters MoreParameters | &

# Tokens

    FUNCTION = r'\w+'
    VARIABLE = r'var'
    LOG_OR = r'or'
    LOG_AND = r'and'
    LOG_GREATER_THAN = r'>'
    LOG_GREATER_THAN_EQUAL = r'>='
    LOG_LESS_THAN = r'<'
    LOG_LESS_THAN_EQUAL = r'<='
    ARIT_PLUS = r'+'
    ARIT_MINUS = r'-'
    L_PARENTESIS = r'('
    R_PARENTESIS = r')'
    COMMA = r','
    INTEGER = r'\d'
    FLOAT = r'\d\.\d'
    STRING = r'\w+'