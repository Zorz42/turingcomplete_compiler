from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Keywords, Token
from jaclang.parser.expression import ExpressionFactory
from jaclang.parser.expression.value import ValueBranch
from jaclang.parser.scope import BranchInScope, BranchInScopeFactory, ScopeFactory, ScopeContext, TokenExpectedException


class WriteBranch(BranchInScope):
    def __init__(self, address: ValueBranch, value: ValueBranch):
        self.address = address
        self.value = value

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        instructions = self.address.generateInstructions(context)
        instructions += [
            Instructions.Push(Registers.RETURN),
        ]
        instructions += self.value.generateInstructions(context)
        instructions += [
            Instructions.Pop(Registers.EXPRESSION),
            Instructions.MemoryWrite(Registers.EXPRESSION, 0, Registers.RETURN),
        ]

        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "Write:")
        print('    ' * nested_level, f"    address:")
        self.address.printInfo(nested_level + 1)
        print('    ' * nested_level, f"    value:")
        self.value.printInfo(nested_level + 1)


class WriteFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] is not Keywords.WRITE:
            raise TokenExpectedException(tokens[pos].pos, "Expected write keyword")

        pos += 1

        expression_factory = ExpressionFactory()
        pos, address = expression_factory.parseExpect(pos, tokens)
        pos, value = expression_factory.parseExpect(pos, tokens)

        return pos, WriteBranch(address, value)

def load():
    ScopeFactory.factories.append(WriteFactory())