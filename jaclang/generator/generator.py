from abc import abstractmethod
from typing import Optional


class Parameter:
    @abstractmethod
    def getInfo(self) -> str:
        pass


class RegisterParameter(Parameter):
    def __init__(self, register_number: int, name: str, raw_name: str):
        self.register_number = register_number
        self.name = name
        self.raw_name = raw_name

    def getInfo(self) -> str:
        return self.name


class Registers:
    RETURN = RegisterParameter(0, "RRET", "ra")
    REG1 = RegisterParameter(1, "R1", "rb")
    REG2 = RegisterParameter(2, "R2", "rc")
    REG3 = RegisterParameter(3, "R3", "rd")
    REG4 = RegisterParameter(4, "R4", "re")
    EXPRESSION = RegisterParameter(5, "REXPR", "rf")
    STACK_BASE = RegisterParameter(6, "RSB", "rg")
    STACK_TOP = RegisterParameter(7, "RSP", "rsp")


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

    @abstractmethod
    def intoRawAssembly(self) -> str:
        pass


def generate_raw_assembly(instruction_label: str, a: Optional[Parameter], b: Optional[Parameter], c: Optional[Parameter]) -> str:
    str1 = instruction_label
    strs = []
    for i, param in enumerate([a, b, c]):
        if param is None:
            strs.append("_")
        elif isinstance(param, ValueParameter):
            strs.append(str(param.value))
            str1 += f"|VAL{i + 1}"
        elif isinstance(param, LabelParameter):
            strs.append(param.label_name)
            str1 += f"|VAL{i + 1}"
        elif isinstance(param, RegisterParameter):
            strs.append(param.raw_name)

    return " ".join([str1] + strs) + "\n"


def generate(instructions: list[Instruction], debug_output: bool = False) -> str:
    if debug_output:
        print("Generated assembly code:")
        print("---------------------------------")
        for instruction in instructions:
            instruction.printInfo()
        print("---------------------------------")

    assembly = ""
    for instruction in instructions:
        assembly += instruction.intoRawAssembly()

    return assembly
