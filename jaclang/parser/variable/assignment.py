from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Registers, Instructions
from jaclang.lexer import IdentifierToken, Token, Symbols
from jaclang.parser.expression.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.root import SymbolData
from jaclang.parser.scope import BranchInScope, ScopeContext, BranchInScopeFactory, TokenExpectedException


class VariableData(SymbolData):
    def __init__(self, pos_on_stack: int):
        self.pos_on_stack = pos_on_stack


class GlobalVariableData(SymbolData):
    def __init__(self):
        pass


class VariableAssignmentBranch(BranchInScope):
    def __init__(self, variable_name: str, value: Optional[ValueBranch]):
        self.variable_name = variable_name
        self.value = value

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        if self.variable_name not in context.symbols.keys():
            raise JaclangSyntaxError(-1, f"Variable '{self.variable_name}' not found")
        variable_obj = context.symbols[self.variable_name]
        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(context)
        if type(variable_obj) is VariableData:
            if self.value is not None:
                instructions += [
                    Instructions.MemoryWrite(Registers.STACK_BASE, variable_obj.pos_on_stack, Registers.RETURN),
                ]
        elif type(variable_obj) is GlobalVariableData:
            if self.value is not None:
                instructions += [
                    Instructions.ImmediateLabel(Registers.ADDRESS, f"var {self.variable_name}"),
                    Instructions.MemoryWrite(Registers.ADDRESS, 0, Registers.RETURN),
                ]
        else:
            raise JaclangSyntaxError(-1, f"Label '{self.variable_name}' is not a variable")

        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "VariableAssignment:")
        print('    ' * nested_level, f"    name: {self.variable_name}")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class VariableAssignmentFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != Symbols.ASSIGNMENT:
            raise TokenExpectedException(tokens[pos].pos, "Expected '='")
        pos += 1
        expression_factory = ExpressionFactory()
        pos, value = expression_factory.parseExpect(pos, tokens)
        return pos, VariableAssignmentBranch(variable_name, value)
