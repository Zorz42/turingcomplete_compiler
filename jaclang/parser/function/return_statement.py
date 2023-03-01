from typing import Optional

from jaclang.generator import Instruction, Instructions
from jaclang.generator.generator import LabelParameter
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
            Instructions.Jump(LabelParameter(f"func_{context.curr_function}_return"), None),
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
