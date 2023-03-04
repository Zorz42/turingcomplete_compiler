from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, Keywords
from jaclang.parser.expression import ValueFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import BranchInScopeFactory, TokenExpectedException, BranchInScope, ScopeContext


class ReceiveKeyBranch(ValueBranch):
    def __init__(self):
        pass

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "receive_key")

    def generateInstructions(self, _: ScopeContext) -> list[Instruction]:
        return [
            Instructions.ReceiveKey(Registers.RETURN)
        ]


class ReceiveKeyFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] is not Keywords.RECV_KEY:
            raise TokenExpectedException(tokens[pos].pos, "Expected receive_key")
        pos += 1
        return pos, ReceiveKeyBranch()


def load():
    ValueFactory.factories.append(ReceiveKeyFactory())
