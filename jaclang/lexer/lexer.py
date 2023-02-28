from __future__ import annotations

from copy import copy
from abc import abstractmethod


class Token:
    def __init__(self):
        self.pos = -1

    @abstractmethod
    def getInfo(self) -> str:
        pass


class SymbolToken(Token):
    symbols = []

    def __init__(self, name: str, identifier: str):
        super().__init__()
        self.name = name
        self.identifier = identifier
        SymbolToken.symbols.append(self)

    def getInfo(self) -> str:
        return self.name

    def __hash__(self):
        return self.identifier.__hash__()

    def __eq__(self, other):
        if type(other) is not SymbolToken:
            return False
        return self.identifier == other.identifier


class IdentifierToken(Token):
    def __init__(self, identifier: str):
        super().__init__()
        self.identifier = identifier

    def getInfo(self) -> str:
        return f"ident: {self.identifier}"

    def __hash__(self):
        return self.identifier.__hash__()

    def __eq__(self, other):
        if type(other) is not IdentifierToken:
            return False
        return self.identifier == other.identifier


class ConstantToken(Token):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def getInfo(self) -> str:
        return f"value: {self.value}"

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, other):
        if type(other) is not ConstantToken:
            return False
        return self.value == other.value


class KeywordToken(Token):
    keywords = {}

    def __init__(self, name: str, identifier: str):
        super().__init__()
        self.name = name
        self.identifier = identifier
        KeywordToken.keywords[identifier] = self

    def getInfo(self) -> str:
        return self.name

    def __hash__(self):
        return self.identifier.__hash__()

    def __eq__(self, other):
        if type(other) is not KeywordToken:
            return False
        return self.identifier == other.identifier


class EndToken(Token):
    def __init__(self):
        super().__init__()

    def getInfo(self) -> str:
        return "END"

    def __hash__(self):
        return "EndToken".__hash__()

    def __eq__(self, other):
        return type(other) is EndToken


class Symbols:
    # Operators
    BIT_SHIFT_LEFT = SymbolToken("BIT_SHIFT_LEFT", "<<")
    BIT_SHIFT_RIGHT = SymbolToken("BIT_SHIFT_LEFT", ">>")
    OR = SymbolToken("OR", "|")
    XOR = SymbolToken("XOR", "^")
    AND = SymbolToken("AND", "&")
    XNOR = SymbolToken("XNOR", "!^")
    NAND = SymbolToken("NAND", "!&")
    INCREMENT = SymbolToken("INCREMENT", "++")
    DECREMENT = SymbolToken("DECREMENT", "--")
    INCREMENT_BY = SymbolToken("INCREMENT_BY", "+=")
    DECREMENT_BY = SymbolToken("DECREMENT_BY", "-=")
    PLUS = SymbolToken("PLUS", "+")
    MINUS = SymbolToken("MINUS", "-")

    # Comparisons
    EQUALS = SymbolToken("EQUALS", "==")
    LESS_OR_EQUAL_THAN = SymbolToken("LESS_OR_EQUAL_THAN", "<=")
    GREATER_OR_EQUAL_THAN = SymbolToken("GREATER_OR_EQUAL_THAN", ">=")
    NOT_EQUAL = SymbolToken("NOT_EQUAL", "!=")
    ASSIGNMENT = SymbolToken("ASSIGNMENT", "=")
    LESS_THAN = SymbolToken("LESS_THAN", "<")
    GREATER_THAN = SymbolToken("GREATER_THAN", ">")

    # Symbols
    LEFT_BRACKET = SymbolToken("LEFT_BRACKET", "(")
    RIGHT_BRACKET = SymbolToken("RIGHT_BRACKET", ")")
    LEFT_BRACE = SymbolToken("LEFT_BRACE", "{")
    RIGHT_BRACE = SymbolToken("RIGHT_BRACE", "}")
    SQUARE_LEFT_BRACKET = SymbolToken("SQUARE_LEFT_BRACKET", "[")
    SQUARE_RIGHT_BRACKET = SymbolToken("SQUARE_RIGHT_BRACKET", "]")


class Keywords:
    FUNC = KeywordToken("FUNC", "func")
    IF = KeywordToken("IF", "if")
    WHILE = KeywordToken("WHILE", "while")
    VAR = KeywordToken("VAR", "var")
    RETURN = KeywordToken("RETURN", "return")


def tokenize(code: str, debug_output: bool = False) -> list[Token]:
    tokens = []
    curr_token = ""

    i = 0
    while i < len(code):
        curr_symbol = None
        for symbol in SymbolToken.symbols:
            if symbol.identifier != "" and code.startswith(symbol.identifier, i):
                curr_symbol = copy(symbol)
                break

        if code[i] == ' ' or curr_symbol is not None:
            if curr_token != "":
                if curr_token.isdigit():
                    new_token = ConstantToken(int(curr_token))
                elif curr_token in KeywordToken.keywords.keys():
                    new_token = KeywordToken.keywords[curr_token]
                else:
                    new_token = IdentifierToken(curr_token)
                new_token.pos = i - len(curr_token)
                curr_token = ""
                tokens.append(new_token)

            if code[i] == ' ':
                i += 1

            if curr_symbol is not None:
                curr_symbol.pos = i
                tokens.append(curr_symbol)
                i += len(curr_symbol.identifier)
        else:
            curr_token += code[i]
            i += 1

    end_token = EndToken()
    end_token.pos = len(code)
    tokens.append(end_token)
    if debug_output:
        print("Generated tokens:")
        print("---------------------------------")
        for token in tokens:
            print(token.getInfo())
        print("---------------------------------")
    return tokens
