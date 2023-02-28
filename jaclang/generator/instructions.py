from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator.generator import Instruction, EmptyByteParameter, RegisterParameter, Value16Parameter, Value8Parameter


class CompareFlags:
    EQUAL = 0b100
    GREATER = 0b001
    LESSER = 0b010
    LESSER_OR_EQUAL = LESSER | EQUAL
    GREATER_OR_EQUAL = GREATER | EQUAL
    NOT_EQUAL = GREATER | LESSER


class Instructions:
    class Terminate(Instruction):
        def __init__(self):
            super().__init__("NOP", 0b00000, [EmptyByteParameter()], 2)

    class Add(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("ADD", 0b00001, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} + {self.reg_b.getInfo()}")

    class Subtract(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("SUB", 0b00010, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} - {self.reg_b.getInfo()}")

    class BitShiftLeft(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("BSL", 0b00011, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} << {self.reg_b.getInfo()}")

    class BitShiftRight(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("BSR", 0b00100, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} >> {self.reg_b.getInfo()}")

    class Or(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("OR", 0b00101, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} OR {self.reg_b.getInfo()}")

    class And(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("AND", 0b00111, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} AND {self.reg_b.getInfo()}")

    class Xor(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("XOR", 0b00110, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} XOR {self.reg_b.getInfo()}")

    class Not(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("NOT", 0b01000, [reg_a, EmptyByteParameter(), reg_save], 4)
            self.reg_a = reg_a
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = NOT {self.reg_a.getInfo()}")

    class Xnor(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("XNOR", 0b01001, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} XNOR {self.reg_b.getInfo()}")

    class Nand(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("NAND", 0b01010, [reg_a, reg_b, reg_save], 4)
            self.reg_a = reg_a
            self.reg_b = reg_b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} NAND {self.reg_b.getInfo()}")

    class MemoryWrite(Instruction):
        def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_value: RegisterParameter):
            super().__init__("MEMW", 0b01011, [reg_addr, reg_value, Value8Parameter(addr_offset)], 4)
            self.reg_addr = reg_addr
            self.addr_offset = addr_offset
            self.reg_value = reg_value

        def printInfo(self):
            print(f"    [{self.reg_addr.getInfo()} + {self.addr_offset}] = {self.reg_value.getInfo()}")

    class MemRead(Instruction):
        def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_save: RegisterParameter):
            super().__init__("MEMR", 0b01100, [reg_addr, Value8Parameter(addr_offset), reg_save], 4)
            self.reg_addr = reg_addr
            self.addr_offset = addr_offset
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = [{self.reg_addr.getInfo()} + {self.addr_offset}]")

    class Immediate(Instruction):
        def __init__(self, reg_save: RegisterParameter, value: int):
            super().__init__("IMM", 0b01101, [reg_save, Value16Parameter(value)], 4)
            self.reg_save = reg_save
            self.value = value

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.value}")

    class ImmediateLabel(Instruction):
        def __init__(self, reg_save: RegisterParameter, label_name: str):
            super().__init__("IMM", 0b01101, [], 4)
            self.reg_save = reg_save
            self.label_name = label_name

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = label {self.label_name}")

        def toBytes(self, labels: dict[str, int]) -> list[int]:
            if self.label_name not in labels.keys():
                raise JaclangSyntaxError(-1, f"Undefined symbol '{self.label_name}'")
            value = labels[self.label_name]
            return [self.opcode] + self.reg_save.toBytes() + Value16Parameter(value).toBytes()

    class Mov(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
            super().__init__("MOV", 0b01110, [reg_a, EmptyByteParameter(), reg_save], 4)
            self.reg_a = reg_a
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()}")

    class Compare(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, flags: int):
            super().__init__("CMP", 0b01111, [reg_a, reg_b, Value8Parameter(flags)], 4)

    class Jump(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("JMP", 0b10000, [reg, Value8Parameter(1), EmptyByteParameter()], 4)

    class JumpIf(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("JMP", 0b10000, [reg, Value8Parameter(0), EmptyByteParameter()], 4)

    class GpuDraw(Instruction):
        def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter):
            super().__init__("GPU_DRAW", 0b10001, [reg_a, reg_b, EmptyByteParameter()], 4)

    class GpuDisplay(Instruction):
        def __init__(self):
            super().__init__("GPU_DISPLAY", 0b10010, [EmptyByteParameter()], 2)

    class Push(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("PUSH", 0b10011, [EmptyByteParameter(), reg, EmptyByteParameter()], 4)

    class Pop(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("POP", 0b10100, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)

    class SetStackPointer(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("SETSP", 0b10101, [reg], 2)
            self.reg = reg

        def printInfo(self):
            print(f"    SP = {self.reg.getInfo()}")

    class GetStackPointer(Instruction):
        def __init__(self, reg: RegisterParameter):
            super().__init__("GETSP", 0b10110, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)
            self.reg = reg

        def printInfo(self):
            print(f"    {self.reg.getInfo()} = SP")

    class Label(Instruction):
        def __init__(self, label_name: str):
            super().__init__("", 0b00000, [], 0)
            self.label_name = label_name

        def printInfo(self):
            print(f"{self.label_name}:")

        def preCompile(self, curr_addr: int, labels: dict[str, int]):
            labels[self.label_name] = curr_addr

    class Value(Instruction):
        def __init__(self, value: int):
            super().__init__("", 0b00000, [], 2)
            self.value = value

        def printInfo(self):
            print(f"    {self.value}")

        def toBytes(self, _: dict[str, int]) -> list[int]:
            return [self.value & 0xFF, (self.value >> 8) & 0xFF]
