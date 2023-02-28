from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, ConstantToken
from jaclang.parser.expression import ValueFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import BranchInScopeFactory, TokenExpectedException, BranchInScope, ScopeContext


class IntegerBranch(ValueBranch):
    def __init__(self, value: int):
        self.value = value

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, self.value)

    def generateInstructions(self, _: ScopeContext) -> list[Instruction]:
        return [Instructions.Immediate(Registers.RETURN, self.value)]


class IntegerFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if type(tokens[pos]) is not ConstantToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected integer")
        value = tokens[pos].value
        pos += 1
        return pos, IntegerBranch(value)


def load():
    ValueFactory.factories.append(IntegerFactory())
