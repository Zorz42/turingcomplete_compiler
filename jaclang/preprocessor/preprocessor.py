from jaclang.error.syntax_error import JaclangSyntaxError


def removeSingleLineComments(code: str) -> str:
    new_code = ""
    is_in_comment = False
    for i, c in enumerate(code):
        if i < len(code) - 1 and c == '/' and code[i + 1] == '/':
            is_in_comment = True

        if c == '\n':
            is_in_comment = False

        new_code += " " if is_in_comment else c

    return new_code


def removeMultilineComments(code: str) -> str:
    new_code = ""
    comment_nesting = 0
    for i, c in enumerate(code):
        if i < len(code) - 1 and c == '/' and code[i + 1] == '*':
            comment_nesting += 1

        if i > 1 and code[i - 2] == '*' and code[i - 1] == '/':
            if comment_nesting > 0:
                comment_nesting -= 1
            else:
                raise JaclangSyntaxError(i - 2, "Closed unopened multiline comment")

        new_code += c if comment_nesting == 0 else " "

    return new_code


def preprocess(file_contents: str, debug_output: bool = False) -> str:
    file_contents = removeSingleLineComments(file_contents)
    file_contents = removeMultilineComments(file_contents)

    if debug_output:
        print("Preprocessed code:")
        print("---------------------------------")
        print(file_contents)
        print("---------------------------------")

    file_contents = file_contents.replace("\n", " ").replace("\t", " ")
    return file_contents
