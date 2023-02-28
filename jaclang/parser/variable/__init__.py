from jaclang.parser import ValueFactory, RootFactory
from jaclang.parser.scope import ScopeFactory
from jaclang.parser.variable.assignment import VariableAssignmentFactory
from jaclang.parser.variable.declaration import VariableDeclarationFactory, GlobalVariableDeclarationFactory
from jaclang.parser.variable.value import VariableFactory


def load():
    ValueFactory.factories.append(VariableFactory())
    ScopeFactory.factories.append(VariableDeclarationFactory())
    ScopeFactory.factories.append(VariableAssignmentFactory())
    RootFactory.factories.append(GlobalVariableDeclarationFactory())
