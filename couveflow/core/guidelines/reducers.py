from couveflow.core.guidelines.structures import (ArithmeticOperator,
                                                  ArithmeticSequence,
                                                  LogicalOperator,
                                                  LogicalSequence, Operand,
                                                  RelationalOperator)


class LogicalReducer:
    @staticmethod
    def reduce(base: bool, sequence: LogicalSequence) -> bool:
        result = base
        for operator, value in sequence:
            match operator:
                case LogicalOperator.AND:
                    result &= value
                case LogicalOperator.OR:
                    result |= value
                case _:
                    raise ValueError(
                        f"Invalid Logical operator: {operator}")

        return result


class RelationalReducer:
    @staticmethod
    def reduce(first: Operand, operator: RelationalOperator, second: Operand) -> bool:
        match operator:
            case RelationalOperator.EQ:
                return first == second
            case RelationalOperator.DIFF:
                return first != second
            case RelationalOperator.LT:
                return first < second
            case RelationalOperator.LTE:
                return first <= second
            case RelationalOperator.GT:
                return first > second
            case RelationalOperator.GTE:
                return first >= second
            case _:
                raise ValueError(
                    f"Invalid Relational operator: {operator}")


class ArithmeticReducer:
    @staticmethod
    def reduce(base: Operand, sequence: ArithmeticSequence) -> Operand:
        result = base
        for operator, value in sequence:
            match operator:
                case ArithmeticOperator.SUM:
                    result += value
                case ArithmeticOperator.SUB:
                    result -= value
                case _:
                    raise ValueError(
                        f"Invalid Arithmetic operator: {operator}")

        return result
