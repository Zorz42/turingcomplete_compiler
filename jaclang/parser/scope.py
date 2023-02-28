from abc import abstractmethod, ABC
from copy import copy

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction
from jaclang.lexer import Token, Symbols, EndToken
from jaclang.parser.root import SymbolData, RootContext, IdManager


class StackManager:
    def __init__(self):
        self.top = 0

    def allocate(self):
        self.top += 2
        return self.top - 2

    def getSize(self):
        return self.top


class ScopeContext(RootContext):
    def __init__(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: StackManager):
        super().__init__(symbols, id_manager)
        self.stack_manager = stack_manager


class BranchInScope:
    @abstractmethod
    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        pass

    @abstractmethod
    def printInfo(self, nested_level: int):
        pass


# modifier branch is a branch that affects execution of the next branch such as if statement
class ModifierBranchInScope(BranchInScope, ABC):
    def __init__(self):
        self.branch: BranchInScope


class BranchInScopeFactory:
    @abstractmethod
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        pass

    def parseExpect(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as exception:
            raise TokenNeededException(exception.pos, exception.message)

    def parseDontExpect(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as _:
            return pos, None


# Parser did not recognize branch type (throws if you need to have a branch present somewhere)
class TokenExpectedException(JaclangSyntaxError):
    pass


# Parser has already recognized branch type and spotted a syntax error
class TokenNeededException(JaclangSyntaxError):
    pass


class ScopeBranch(BranchInScope):
    def __init__(self, branches: list[BranchInScope]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "scope:")
        for branch in self.branches:
            branch.printInfo(nested_level + 1)

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        copied_context = context
        copied_context.symbols = copy(context.symbols)
        instructions = []
        for branch in self.branches:
            instructions += branch.generateInstructions(copied_context)
        return instructions


class ScopeFactory(BranchInScopeFactory):
    factories = []

    @staticmethod
    def parseStatement(pos: int, tokens: list[Token]) -> (int, BranchInScope):
        for factory in ScopeFactory.factories:
            pos, branch = factory.parseDontExpect(pos, tokens)
            if branch is not None:
                if issubclass(type(branch), ModifierBranchInScope):
                    pos, subbranch = ScopeFactory.parseStatement(pos, tokens)
                    branch.branch = subbranch

                return pos, branch

        if tokens[pos] == EndToken():
            raise TokenNeededException(tokens[pos].pos, "Expected '}' at the end of scope")
        else:
            raise TokenNeededException(tokens[pos].pos, "Did not recognize statement")

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if pos >= len(tokens) or tokens[pos] != Symbols.LEFT_BRACE:
            raise TokenExpectedException(tokens[pos].pos, "Expected '{' at beginning of scope")
        pos += 1

        branches = []
        while tokens[pos] != Symbols.RIGHT_BRACE:
            pos, branch = self.parseStatement(pos, tokens)
            branches.append(branch)
        pos += 1

        return pos, ScopeBranch(branches)


def load():
    ScopeFactory.factories.append(ScopeFactory())
