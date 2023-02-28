from jaclang.generator import Instruction, Instructions, Registers
from jaclang.generator.generator import ValueParameter, LabelParameter
from jaclang.lexer import Token, Keywords
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import ScopeFactory, BranchInScope, BranchInScopeFactory, ModifierBranchInScope, \
    TokenExpectedException, ScopeContext


class WhileStatementBranch(ModifierBranchInScope):
    def __init__(self, condition: ValueBranch):
        super().__init__()
        self.condition = condition

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        while_begin = f"while_begin_{context.id_manager.requestId()}"
        while_begin2 = f"while_begin2_{context.id_manager.requestId()}"
        while_end = f"while_end_{context.id_manager.requestId()}"
        instructions = [
            Instructions.Label(while_begin),
        ]
        instructions += self.condition.generateInstructions(context)
        instructions += [
            Instructions.Jump(LabelParameter(while_begin2), Registers.RETURN),
            Instructions.Jump(LabelParameter(while_end), None),
            Instructions.Label(while_begin2),
        ]
        instructions += self.branch.generateInstructions(context)
        instructions += [
            Instructions.Jump(LabelParameter(while_begin), None),
            Instructions.Label(while_end),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print("    " * nested_level, "WhileStatement:")
        self.condition.printInfo(nested_level + 1)
        self.branch.printInfo(nested_level + 1)


class WhileStatementFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] != Keywords.WHILE:
            raise TokenExpectedException(tokens[pos].pos, "Expected while keyword")
        pos += 1

        expr_factory = ExpressionFactory()
        pos, condition = expr_factory.parseExpect(pos, tokens)

        return pos, WhileStatementBranch(condition)


def load():
    ScopeFactory.factories.append(WhileStatementFactory())
