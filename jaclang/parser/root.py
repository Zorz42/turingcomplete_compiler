from abc import abstractmethod

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions
from jaclang.lexer import Token, EndToken


class SymbolData:
    pass


class IdManager:
    def __init__(self):
        self.curr_id = 0

    def requestId(self):
        result = self.curr_id
        self.curr_id += 1
        return result


class RootContext:
    def __init__(self, symbols: dict[str, SymbolData], id_manager: IdManager):
        self.symbols = symbols
        self.id_manager = id_manager


class BranchInRoot:
    @abstractmethod
    def generateInstructions(self, context: RootContext) -> list[Instruction]:
        pass

    @abstractmethod
    def printInfo(self, nested_level: int):
        pass


class BranchInRootFactory:
    @abstractmethod
    def parse(self, pos: int, tokens: list[Token]) -> (int, BranchInRoot):
        pass


class InitGenerator:
    def generateInitInstructions(self, context: RootContext) -> list[Instruction]:
        return []


class RootBranch:
    init_generators: list[InitGenerator] = []

    def __init__(self, branches: list[BranchInRoot]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        for branch in self.branches:
            branch.printInfo(nested_level)

    def generateInstructions(self) -> list[Instruction]:
        instructions = []

        context = RootContext({}, IdManager())
        for branch in self.branches:
            instructions += branch.generateInstructions(context)

        start_instructions = []
        for generator in self.init_generators:
            start_instructions += generator.generateInitInstructions(context)

        start_instructions += [
            Instructions.Terminate()
        ]

        return start_instructions + instructions


class RootFactory:
    factories = []

    @staticmethod
    def parse(pos: int, tokens: list[Token]) -> (int, RootBranch):
        branches = []
        while tokens[pos] != EndToken():
            for factory in RootFactory.factories:
                pos, branch = factory.parse(pos, tokens)
                if branch is not None:
                    branches.append(branch)
                    break
            else:
                raise JaclangSyntaxError(tokens[pos].pos, "Unrecognized statement")

        return pos, RootBranch(branches)
