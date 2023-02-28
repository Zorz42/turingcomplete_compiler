from abc import abstractmethod


class Parameter:
    @abstractmethod
    def getInfo(self) -> str:
        pass


class RegisterParameter(Parameter):
    def __init__(self, register_number, name):
        self.register_number = register_number
        self.name = name

    def getInfo(self) -> str:
        return self.name


class Registers:
    RETURN = RegisterParameter(0, "RRET")
    REG1 = RegisterParameter(1, "R1")
    REG2 = RegisterParameter(2, "R2")
    REG3 = RegisterParameter(3, "R3")
    REG4 = RegisterParameter(4, "R4")
    EXPRESSION = RegisterParameter(5, "REXPR")
    STACK_BASE = RegisterParameter(6, "RSB")
    STACK_TOP = RegisterParameter(7, "RSP")


class ValueParameter(Parameter):
    def __init__(self, value: int):
        self.value = value

    def getInfo(self) -> str:
        return str(self.value)


class LabelParameter(Parameter):
    def __init__(self, label_name: str):
        self.label_name = label_name

    def getInfo(self) -> str:
        return "{" + self.label_name + "}"


class Instruction:
    @abstractmethod
    def printInfo(self):
        pass


def generate(instructions: list[Instruction], debug_output: bool = False) -> str:
    if debug_output:
        print("Generated assembly code:")
        print("---------------------------------")
        for instruction in instructions:
            instruction.printInfo()
        print("---------------------------------")

    return ""
