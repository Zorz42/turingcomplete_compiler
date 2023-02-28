from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions
from jaclang.lexer import Token, Keywords, IdentifierToken, Symbols
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.root import BranchInRootFactory, BranchInRoot, RootContext
from jaclang.parser.scope import BranchInScopeFactory, BranchInScope, TokenExpectedException, TokenNeededException, \
    ScopeContext
from jaclang.parser.variable.assignment import VariableAssignmentBranch, GlobalVariableData, VariableData


class VariableDeclarationBranch(BranchInScope):
    def __init__(self, variable_name: str, value: Optional[ValueBranch]):
        self.variable_name = variable_name
        self.assignment = VariableAssignmentBranch(variable_name, value)

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        pos_on_stack = context.stack_manager.allocate()
        context.symbols[self.variable_name] = VariableData(pos_on_stack)

        instructions = []
        if self.assignment is not None:
            instructions += self.assignment.generateInstructions(context)
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "VariableDeclaration:")
        print('    ' * nested_level, f"    name: {self.variable_name}")
        if self.assignment is not None:
            self.assignment.value.printInfo(nested_level + 1)


class VariableDeclarationFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] != Keywords.VAR:
            raise TokenExpectedException(tokens[pos].pos, "Expected var keyword")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] == Symbols.ASSIGNMENT:
            pos += 1
            expression_factory = ExpressionFactory()
            pos, value = expression_factory.parseExpect(pos, tokens)
            return pos, VariableDeclarationBranch(variable_name, value)
        else:
            return pos, VariableDeclarationBranch(variable_name, None)


class GlobalVariableDeclarationBranch(BranchInRoot):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def generateInstructions(self, context: RootContext) -> list[Instruction]:
        context.symbols[self.variable_name] = GlobalVariableData()

        return [
            Instructions.Label(f"var {self.variable_name}"),
            Instructions.Value(0),
        ]

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "GlobalVariableDeclaration:")
        print('    ' * nested_level, f"    name: {self.variable_name}")


class GlobalVariableDeclarationFactory(BranchInRootFactory):
    def parse(self, pos: int, tokens: list[Token]) -> (int, BranchInRoot):
        if tokens[pos] != Keywords.VAR:
            return pos, None

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise JaclangSyntaxError(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1

        return pos, GlobalVariableDeclarationBranch(variable_name)
