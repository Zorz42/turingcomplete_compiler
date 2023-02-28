from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, IdentifierToken, Symbols
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.function.declaration import FunctionData
from jaclang.parser.root import InitGenerator, RootContext
from jaclang.parser.scope import BranchInScope, BranchInScopeFactory, TokenExpectedException, ScopeContext, StackManager


class FunctionCallBranch(ValueBranch):
    def __init__(self, function_name: str, args: list[ValueBranch]):
        self.function_name = function_name
        self.args = args

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"call: {self.function_name}")
        for arg in self.args:
            print('    ' * nested_level, "arg:")
            arg.printInfo(nested_level + 1)

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        if self.function_name not in context.symbols.keys():
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' undefined")

        if type(context.symbols[self.function_name]) is not FunctionData:
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' is not a function")

        func = context.symbols[self.function_name]
        if func.args_num != len(self.args):
            raise JaclangSyntaxError(-1, f"Incorrect number of arguments on a function call (got {len(self.args)}, expected {func.args_num})")

        jmp_label = f"jump {context.id_manager.requestId()}"
        instructions = []
        for arg in self.args:
            instructions += arg.generateInstructions(context)
            instructions += [
                Instructions.Push(Registers.RETURN),
            ]

        instructions += [
            Instructions.ImmediateLabel(Registers.ADDRESS, jmp_label),
            Instructions.Push(Registers.ADDRESS),
            Instructions.ImmediateLabel(Registers.ADDRESS, "func " + self.function_name),
            Instructions.Jump(Registers.ADDRESS),
            Instructions.Label(jmp_label),
        ]

        instructions += [
            Instructions.Pop(Registers.ADDRESS),
        ] * len(self.args)
        return instructions


class FunctionCallFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        function_name = tokens[pos].identifier
        pos += 1
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        expr_factory = ExpressionFactory()
        args = []
        pos += 1
        while tokens[pos] != Symbols.RIGHT_BRACKET:
            pos, branch = expr_factory.parseExpect(pos, tokens)
            args.append(branch)

        pos += 1
        return pos, FunctionCallBranch(function_name, args)


class MainCallGenerator(InitGenerator):
    def generateInitInstructions(self, context: RootContext) -> list[Instruction]:
        return FunctionCallBranch("main", []).generateInstructions(
            ScopeContext(context.symbols, context.id_manager, StackManager()))
