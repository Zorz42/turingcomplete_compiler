from abc import abstractmethod


class Parameter:
    @abstractmethod
    def toBytes(self) -> list[int]:
        pass

    @abstractmethod
    def getInfo(self) -> str:
        pass


class RegisterParameter(Parameter):
    def __init__(self, register_number, name):
        self.register_number = register_number
        self.name = name

    def toBytes(self) -> list[int]:
        return [self.register_number]

    def getInfo(self) -> str:
        return self.name


class Registers:
    RETURN = RegisterParameter(0, "RRET")
    REG1 = RegisterParameter(1, "R1")
    REG2 = RegisterParameter(2, "R2")
    REG3 = RegisterParameter(3, "R3")
    REG4 = RegisterParameter(4, "R4")
    ADDRESS = RegisterParameter(5, "RADDR")
    EXPRESSION = RegisterParameter(6, "REXPR")
    STACK_BASE = RegisterParameter(7, "RSB")


class Value16Parameter(Parameter):
    def __init__(self, value: int):
        self.value = value

    def toBytes(self) -> list[int]:
        return [self.value & 0xFF, (self.value >> 8) & 0xFF]

    def getInfo(self) -> str:
        return str(self.value)


class Value8Parameter(Parameter):
    def __init__(self, value: int):
        self.value = value

    def toBytes(self) -> list[int]:
        return [self.value & 0xFF]

    def getInfo(self) -> str:
        return str(self.value)


class EmptyByteParameter(Parameter):
    def toBytes(self) -> list[int]:
        return [0]

    def getInfo(self) -> str:
        return ""


class Instruction:
    def __init__(self, name: str, opcode: int, params: list[Parameter], length: int):
        self.name = name
        self.opcode = opcode
        self.params = params
        self.length = length
        if length not in [0, 2, 4]:
            raise Exception("Instruction length must be either 0, 2 or 4")

    def printInfo(self):
        info = "    " + self.name + " "
        for param in self.params:
            param_info = param.getInfo()
            info += param.getInfo()
            if param_info:
                info += " "
        print(info)

    def toBytes(self, _: dict[str, int]) -> list[int]:
        if self.length == 0:
            return []

        byte_arr = [self.opcode]
        for param in self.params:
            byte_arr += param.toBytes()

        if len(byte_arr) != self.length:
            raise Exception("Byte array length must match")

        return byte_arr

    def preCompile(self, curr_addr: int, labels: dict[str, int]):
        pass


def generate(instructions: list[Instruction], debug_output: bool = False) -> str:
    if debug_output:
        print("Generated assembly code:")
        print("---------------------------------")
        for instruction in instructions:
            instruction.printInfo()
        print("---------------------------------")
    binary_code = []
    curr_addr = 0
    labels = {}

    for instruction in instructions:
        instruction.preCompile(curr_addr, labels)
        curr_addr += instruction.length

    for instruction in instructions:
        binary_code += instruction.toBytes(labels)

    return ""
