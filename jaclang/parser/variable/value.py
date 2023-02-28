from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, IdentifierToken
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import ScopeContext, BranchInScopeFactory, BranchInScope, TokenExpectedException
from jaclang.parser.variable.assignment import VariableData, GlobalVariableData


class VariableBranch(ValueBranch):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"var: {self.variable_name}")

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        if self.variable_name not in context.symbols.keys():
            raise JaclangSyntaxError(-1, f"Variable '{self.variable_name}' not found")
        variable_obj = context.symbols[self.variable_name]
        if type(variable_obj) is VariableData:
            return [
                Instructions.MemRead(Registers.STACK_BASE, variable_obj.pos_on_stack, Registers.RETURN),
            ]
        elif type(variable_obj) is GlobalVariableData:
            return [
                Instructions.ImmediateLabel(Registers.ADDRESS, f"var {self.variable_name}"),
                Instructions.MemRead(Registers.ADDRESS, 0, Registers.RETURN),
            ]
        else:
            raise JaclangSyntaxError(-1, f"Label '{self.variable_name}' is not a variable")


class VariableFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        variable_name = tokens[pos].identifier
        pos += 1
        return pos, VariableBranch(variable_name)
