from abc import abstractmethod

from jaclang.generator import Instructions, Registers, Instruction, CompareFlags
from jaclang.lexer import Symbols


class Operator:
    operators = {}

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generateInstructions(self) -> list[Instruction]:
        pass


class PlusOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Add(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class MinusOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Subtract(Registers.RETURN, Registers.EXPRESSION, Registers.RETURN)]


class EqualsOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.EQUAL)]


class LesserOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.LESSER)]


class GreaterOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.GREATER)]


class LesserOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.LESSER_OR_EQUAL)]


class GreaterOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.GREATER_OR_EQUAL)]


class NotEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.NOT_EQUAL)]


class BitShiftLeftOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.BitShiftLeft(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class BitShiftRightOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.BitShiftRight(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class OrOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Or(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class XorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Xor(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class AndOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.And(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class XnorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Xnor(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class NandOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Nand(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


Operator.operators[Symbols.PLUS] = PlusOperator(Symbols.PLUS.name)
Operator.operators[Symbols.MINUS] = MinusOperator(Symbols.MINUS.name)
Operator.operators[Symbols.EQUALS] = EqualsOperator(Symbols.EQUALS.name)
Operator.operators[Symbols.LESS_THAN] = LesserOperator(Symbols.LESS_THAN.name)
Operator.operators[Symbols.GREATER_THAN] = GreaterOperator(Symbols.GREATER_THAN.name)
Operator.operators[Symbols.LESS_OR_EQUAL_THAN] = LesserOrEqualOperator(Symbols.LESS_OR_EQUAL_THAN.name)
Operator.operators[Symbols.GREATER_OR_EQUAL_THAN] = GreaterOrEqualOperator(Symbols.GREATER_OR_EQUAL_THAN.name)
Operator.operators[Symbols.NOT_EQUAL] = NotEqualOperator(Symbols.NOT_EQUAL.name)
Operator.operators[Symbols.BIT_SHIFT_LEFT] = BitShiftLeftOperator(Symbols.BIT_SHIFT_LEFT.name)
Operator.operators[Symbols.BIT_SHIFT_RIGHT] = BitShiftRightOperator(Symbols.BIT_SHIFT_RIGHT.name)
Operator.operators[Symbols.OR] = OrOperator(Symbols.OR.name)
Operator.operators[Symbols.XOR] = XorOperator(Symbols.XOR.name)
Operator.operators[Symbols.AND] = AndOperator(Symbols.AND.name)
Operator.operators[Symbols.XNOR] = XnorOperator(Symbols.XNOR.name)
Operator.operators[Symbols.NAND] = NandOperator(Symbols.NAND.name)
