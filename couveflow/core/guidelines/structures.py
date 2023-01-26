from enum import Enum, auto
from typing import List, Tuple, Union


class RelationalOperator(Enum):
    EQ = auto()
    DIFF = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()


class LogicalOperator(Enum):
    AND = auto()
    OR = auto()


class ArithmeticOperator(Enum):
    SUM = auto()
    SUB = auto()


Operand = Union[int, float, str]
ArithmeticSequence = List[Tuple[ArithmeticOperator, Operand]]
LogicalSequence = List[Tuple[LogicalOperator, bool]]
