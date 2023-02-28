from jaclang.lexer import Symbols, Token
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.scope import BranchInScopeFactory, BranchInScope, TokenExpectedException


class ParenthesesFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1

        expr_factory = ExpressionFactory()
        pos, expr = expr_factory.parseExpect(pos, tokens)

        if tokens[pos] != Symbols.RIGHT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected ')'")

        pos += 1

        return pos, expr
