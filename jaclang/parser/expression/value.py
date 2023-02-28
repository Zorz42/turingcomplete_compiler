from abc import ABC

from jaclang.lexer import Token
from jaclang.parser.scope import BranchInScope, BranchInScopeFactory, TokenExpectedException


class ValueBranch(BranchInScope, ABC):
    pass


class ValueFactory(BranchInScopeFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        for factory in ValueFactory.factories:
            pos, value = factory.parseDontExpect(pos, tokens)
            if value is not None:
                return pos, value

        raise TokenExpectedException(tokens[pos].pos, "Expected value")
