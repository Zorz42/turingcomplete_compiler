from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser import expression
from jaclang.parser import function
# modules
from jaclang.parser import if_statement, while_statement
from jaclang.parser import integer
from jaclang.parser import pointers
from jaclang.parser import scope
from jaclang.parser import variable
from jaclang.parser import receive_key
from jaclang.parser.expression import ValueFactory
from jaclang.parser.root import RootFactory

while_statement.load()
if_statement.load()
integer.load()
function.load()
scope.load()
variable.load()
pointers.load()
receive_key.load()
expression.load()


def parse(tokens: list[Token], debug_output: bool = False) -> list[Instruction]:
    root_factory = RootFactory()

    _, root_branch = root_factory.parse(0, tokens)

    if debug_output:
        print("Generated abstract syntax tree:")
        print("---------------------------------")
        root_branch.printInfo(0)
        print("---------------------------------")

    return root_branch.generateInstructions()
