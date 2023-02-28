from jaclang.parser.expression.expression import ExpressionFactory
from jaclang.parser.expression.parentheses import ParenthesesFactory
from jaclang.parser.expression.value import ValueFactory
from jaclang.parser.scope import ScopeFactory


def load():
    ScopeFactory.factories.append(ExpressionFactory())
    ValueFactory.factories.append(ParenthesesFactory())
