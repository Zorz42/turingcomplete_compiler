import sys

from jaclang import compileJaclang
from jaclang.error.syntax_error import JaclangSyntaxError


def main():
    if len(sys.argv) < 2:
        print(
            """Usage: python3 -m jaclang [input_file] [output_file] [options]
Options:
- debug_preprocess: print preprocessed code
- debug_tokens: print tokens
- debug_tree: print abstract syntax tree
"""
        )
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    options = sys.argv[3:]

    with open(input_file, "r") as file:
        file_contents = file.read()

    try:
        assembly_code = compileJaclang(file_contents, options)

        assembly_num_lines = len(assembly_code.splitlines())
        print(f"Assembly has {assembly_num_lines} lines")

        with open(output_file, "w") as file:
            file.write(assembly_code)

    except JaclangSyntaxError as error:
        error.printError(file_contents)
        exit(1)


if __name__ == "__main__":
    main()
