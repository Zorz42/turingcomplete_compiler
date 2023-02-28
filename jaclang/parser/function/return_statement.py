from typing import Optional

from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, Keywords
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import BranchInScope, BranchInScopeFactory, TokenExpectedException, ScopeContext


class ReturnStatementBranch(BranchInScope):
    def __init__(self, value: Optional[ValueBranch]):
        self.value = value

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(context)
        instructions += [
            Instructions.Pop(Registers.ADDRESS),
            Instructions.SetStackPointer(Registers.STACK_BASE),
            Instructions.Mov(Registers.ADDRESS, Registers.STACK_BASE),
            Instructions.Pop(Registers.ADDRESS),
            Instructions.Jump(Registers.ADDRESS),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "return:")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class ReturnStatementFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScopeFactory):
        if tokens[pos] != Keywords.RETURN:
            raise TokenExpectedException(pos, "Expected return keyword")

        pos += 1

        expression_factory = ExpressionFactory()
        pos, value_branch = expression_factory.parseDontExpect(pos, tokens)

        return pos, ReturnStatementBranch(value_branch)
