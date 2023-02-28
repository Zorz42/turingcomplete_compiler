RED = '\033[91m'
BOLD = '\033[1m'
CLEAR = '\033[0m'


class JaclangSyntaxError(Exception):
    def __init__(self, pos: int, message: str):
        self.pos = pos
        self.message = message

    def printError(self, file_contents: str):
        print(f"{RED}{BOLD}SyntaxError: {self.message}")
        if self.pos == -1:
            print("Error location not provided")
        else:
            right = self.pos
            left = self.pos

            while right < len(file_contents) and file_contents[right] != '\n':
                right += 1

            while left > 0 and file_contents[left - 1] != '\n':
                left -= 1

            line_num = 1
            for i in range(self.pos):
                if file_contents[i] == "\n":
                    line_num += 1

            line_num_prefix = f"line {line_num}: "
            print(line_num_prefix + file_contents[left:right].replace("\t", " "))
            print(" " * (self.pos - left + len(line_num_prefix)) + "^" + CLEAR)
