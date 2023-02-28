from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token
from jaclang.parser.expression.operators import Operator
from jaclang.parser.expression.value import ValueBranch, ValueFactory
from jaclang.parser.scope import ScopeContext, BranchInScopeFactory, BranchInScope, TokenExpectedException


class ExpressionBranch(ValueBranch):
    def __init__(self, value1: ValueBranch, expr_operator: Operator, value2: ValueBranch):
        self.value1 = value1
        self.value2 = value2
        self.expr_operator = expr_operator

    def printInfo(self, nested_level: int):
        self.value1.printInfo(nested_level)
        print('    ' * nested_level, self.expr_operator.name)
        self.value2.printInfo(nested_level)

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        instructions = []

        instructions += self.value1.generateInstructions(context)
        instructions += [
            Instructions.Mov(Registers.RETURN, Registers.EXPRESSION),
            Instructions.Push(Registers.EXPRESSION),
        ]
        instructions += self.value2.generateInstructions(context)
        instructions += [
            Instructions.Pop(Registers.EXPRESSION),
        ]

        instructions += self.expr_operator.generateInstructions()

        return instructions


class ExpressionFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        value_factory = ValueFactory()
        pos, value = value_factory.parseDontExpect(pos, tokens)
        if value is None:
            raise TokenExpectedException(tokens[pos].pos, "Expected value")

        return self.parseRecursive(pos, tokens, value)

    def parseRecursive(self, pos: int, tokens: list[Token], expr_branch: ValueBranch) -> (int, ValueBranch):
        if tokens[pos] not in Operator.operators.keys():
            return pos, expr_branch

        expr_operator = Operator.operators[tokens[pos]]
        pos += 1
        value_factory = ValueFactory()
        pos, value = value_factory.parseExpect(pos, tokens)
        new_expr_branch = ExpressionBranch(expr_branch, expr_operator, value)

        return self.parseRecursive(pos, tokens, new_expr_branch)
