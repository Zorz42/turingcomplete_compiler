from copy import copy

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions, Registers
from jaclang.generator.generator import ValueParameter
from jaclang.lexer import Token, Keywords, IdentifierToken, Symbols
from jaclang.parser.root import SymbolData, BranchInRoot, BranchInRootFactory, RootContext
from jaclang.parser.scope import ScopeBranch, ScopeFactory, ScopeContext, StackManager
from jaclang.parser.variable.assignment import VariableData


class FunctionData(SymbolData):
    def __init__(self, args_num: int):
        self.args_num = args_num


class FunctionDeclarationBranch(BranchInRoot):
    def __init__(self, name: str, arg_names: list[str], body: ScopeBranch):
        self.name = name
        self.body = body
        self.arg_names = arg_names

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        print('    ' * nested_level, f"    args: {' '.join(self.arg_names)}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self, context: RootContext) -> list[Instruction]:
        context.symbols[self.name] = FunctionData(len(self.arg_names))

        new_context = ScopeContext(copy(context.symbols), context.id_manager, StackManager(), self.name)

        curr_pos_on_stack = -2
        for arg in reversed(self.arg_names):
            new_context.symbols[arg] = VariableData(curr_pos_on_stack)
            curr_pos_on_stack -= 1

        body_instructions = self.body.generateInstructions(new_context)

        begin_instructions: list[Instruction] = [
            Instructions.Label(f"func_{self.name}"),
            Instructions.Push(Registers.STACK_BASE),
            Instructions.Mov(Registers.STACK_TOP, Registers.STACK_BASE),
            Instructions.Add(Registers.STACK_BASE, ValueParameter(new_context.stack_manager.getSize()), Registers.STACK_TOP),
        ]

        return_instructions: list[Instruction] = [
            Instructions.Label(f"func_{self.name}_return"),
            Instructions.Mov(Registers.STACK_BASE, Registers.STACK_TOP),
            Instructions.Pop(Registers.STACK_BASE),
            Instructions.Subtract(Registers.STACK_TOP, ValueParameter(len(self.arg_names)), Registers.STACK_TOP),
            Instructions.Pop(Registers.EXPRESSION),
            Instructions.Jump(Registers.EXPRESSION, None),
        ]

        return begin_instructions + body_instructions + return_instructions


class FunctionDeclarationFactory(BranchInRootFactory):
    def parse(self, pos: int, tokens: list[Token]) -> (int, BranchInRoot):
        if tokens[pos] != Keywords.FUNC:
            return pos, None

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise JaclangSyntaxError(tokens[pos].pos, "Expected identifier after func keyword")
        func_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise JaclangSyntaxError(tokens[pos].pos, "Expected '(' after func name")

        arg_names = []
        pos += 1
        while tokens[pos] != Symbols.RIGHT_BRACKET:
            if type(tokens[pos]) is IdentifierToken:
                arg_names.append(tokens[pos].identifier)
                pos += 1
            else:
                raise JaclangSyntaxError(tokens[pos].pos, "Expected ')' or variable name")

        pos += 1

        pos, body = ScopeFactory().parseExpect(pos, tokens)

        return pos, FunctionDeclarationBranch(func_name, arg_names, body)
