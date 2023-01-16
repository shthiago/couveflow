from ast import literal_eval
from ply import yacc
from couveflow.core.guidelines.functions import get_functions

from couveflow.core.guidelines.lexer import GuidelineLexer
from couveflow.core.guidelines.reducers import ArithmeticReducer, LogicalReducer, RelationalReducer
from couveflow.core.guidelines.structures import ArithmeticOperator, LogicalOperator, RelationalOperator
from couveflow.core.models import Variable


class GuidelineEvaluator:
    def __init__(self, **kwargs):
        self.lexer = GuidelineLexer()
        self.tokens = self.lexer.tokens
        self.yacc = yacc.yacc(module=self, start="Expression", **kwargs)

    def evaluate(self, source_code: str) -> bool:
        return self.yacc.parse(source_code, lexer=self.lexer)

    def p_empty(self, p: yacc.YaccProduction):
        '''empty :'''
        pass

    def p_error(self, p: yacc.YaccProduction):
        print(f"ERROR! {p}")

    def p_expression_to_logical(self, p: yacc.YaccProduction):
        '''Expression : LogicalExpression'''
        p[0] = p[1]

    def p_expression_to_empty(self, p: yacc.YaccProduction):
        '''Expression : empty'''
        p[0] = True

    def p_logical_to_arit(self, p: yacc.YaccProduction):
        '''LogicalExpression : RelationalExpression LogicalExpressionAux'''
        p[0] = LogicalReducer.reduce(p[1], p[2])

    def p_logical_to_arit_loop(self, p: yacc.YaccProduction):
        '''LogicalExpressionAux : LogicalOperator RelationalExpression LogicalExpressionAux'''
        p[0] = [(p[1], p[2])] + p[3]

    def p_logical_to_empty(self, p: yacc.YaccProduction):
        '''LogicalExpressionAux : empty'''
        p[0] = []

    def p_logical_or(self, p: yacc.YaccProduction):
        '''LogicalOperator : LOG_OR'''
        p[0] = LogicalOperator.OR

    def p_logical_and(self, p: yacc.YaccProduction):
        '''LogicalOperator : LOG_AND'''
        p[0] = LogicalOperator.AND

    def p_relational_to_arit(self, p: yacc.YaccProduction):
        '''RelationalExpression : ArithmeticExpression RelationalExpressionAux'''
        if p[2] is None:
            p[0] = p[1] not in [0, '']
        else:
            op, second = p[2]
            p[0] = RelationalReducer.reduce(p[1], op, second)

    def p_relationalaux_loop(self, p: yacc.YaccProduction):
        '''RelationalExpressionAux : RelationalOperator ArithmeticExpression'''
        p[0] = (p[1], p[2])

    def p_relational_empty(self, p: yacc.YaccProduction):
        '''RelationalExpressionAux : empty'''
        p[0] = None

    def p_relational_gt(self, p: yacc.YaccProduction):
        '''RelationalOperator : LOG_GREATER_THAN'''
        p[0] = RelationalOperator.GT

    def p_relational_gte(self, p: yacc.YaccProduction):
        '''RelationalOperator : LOG_GREATER_THAN_EQUAL'''
        p[0] = RelationalOperator.GTE

    def p_relational_lt(self, p: yacc.YaccProduction):
        '''RelationalOperator : LOG_LESS_THAN'''
        p[0] = RelationalOperator.LT

    def p_relational_lte(self, p: yacc.YaccProduction):
        '''RelationalOperator : LOG_LESS_THAN_EQUAL'''
        p[0] = RelationalOperator.LTE

    def p_relational_eq(self, p: yacc.YaccProduction):
        '''RelationalOperator : LOG_EQUAL_TO'''
        p[0] = RelationalOperator.EQ

    def p_arit_to_operator(self, p: yacc.YaccProduction):
        '''ArithmeticExpression : Operand ArithmeticExpressionAux'''
        p[0] = ArithmeticReducer.reduce(p[1], p[2])

    def p_arit_loop(self, p: yacc.YaccProduction):
        '''ArithmeticExpressionAux : ArithmeticOperator Operand ArithmeticExpressionAux'''
        p[0] = [(p[1], p[2])] + p[3]

    def p_arit_empty(self, p: yacc.YaccProduction):
        '''ArithmeticExpressionAux : empty '''
        p[0] = []

    def p_arit_op_plus(self, p: yacc.YaccProduction):
        '''ArithmeticOperator : ARIT_PLUS'''
        p[0] = ArithmeticOperator.SUM

    def p_airt_op_minus(self, p: yacc.YaccProduction):
        '''ArithmeticOperator : ARIT_MINUS'''
        p[0] = ArithmeticOperator.SUB

    def p_operand_native(self, p: yacc.YaccProduction):
        '''Operand : NativeOperand'''
        p[0] = p[1]

    def p_operand_func(self, p: yacc.YaccProduction):
        '''Operand : FuncCall'''
        p[0] = p[1]

    def p_operand_variable(self, p: yacc.YaccProduction):
        '''Operand : Variable'''
        p[0] = p[1]

    def p_native_integer(self, p: yacc.YaccProduction):
        '''NativeOperand : INTEGER'''
        p[0] = int(p[1])

    def p_native_float(self, p: yacc.YaccProduction):
        '''NativeOperand : FLOAT'''
        p[0] = float(p[1])

    def p_native_string(self, p: yacc.YaccProduction):
        '''NativeOperand : STRING'''
        p[0] = p[1]

    def p_funcall(self, p: yacc.YaccProduction):
        '''FuncCall : FUNCTION L_PARENTESIS Parameters R_PARENTESIS'''
        function = get_functions()[p[1]]
        p[0] = function(*p[3])

    def p_variable(self, p: yacc.YaccProduction):
        '''Variable : VARIABLE L_PARENTESIS STRING R_PARENTESIS'''
        var = Variable.objects.get(name=literal_eval(p[3]))
        p[0] = var.value

    def p_parameter(self, p: yacc.YaccProduction):
        '''Parameters : NativeOperand MoreParameters'''
        p[0] = [p[1], *p[2]]

    def p_more_parameters_loop(self, p: yacc.YaccProduction):
        '''MoreParameters : COMMA NativeOperand MoreParameters'''
        p[0] = [p[2], *p[3]]

    def p_more_parameters_empty(self, p: yacc.YaccProduction):
        '''MoreParameters : empty'''
        p[0] = []
