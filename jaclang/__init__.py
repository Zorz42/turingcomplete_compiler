from jaclang.generator import generate
from jaclang.lexer import tokenize
from jaclang.parser import parse
from jaclang.preprocessor import preprocess


def compileJaclang(file_contents: str, options: list[str]) -> str:
    preprocessed_contents = preprocess(file_contents, "debug_preprocess" in options)
    tokens = tokenize(preprocessed_contents, "debug_tokens" in options)
    instructions = parse(tokens, "debug_tree" in options)
    return generate(instructions, "debug_assembly" in options)
