from typing import Optional

from jaclang.generator.generator import RegisterParameter, Instruction, Parameter, generate_raw_assembly, ValueParameter

def format_memory_addr(reg: str, offset: int):
    if offset == 0:
        return f"[{reg}]"
    elif offset > 0:
        return f"[{reg} + {offset}]"
    else:
        return f"[{reg} - {-offset}]"


class Instructions:
    class Noop(Instruction):
        def printInfo(self):
            print("    NOOP")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("NOOP", None, None, None)

    class Add(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} + {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("ADD", self.a, self.b, self.reg_save)

    class Subtract(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} - {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("SUB", self.a, self.b, self.reg_save)

    class Multiply(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} * {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("MUL", self.a, self.b, self.reg_save)

    class Divide(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} / {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("DIV", self.a, self.b, self.reg_save)

    class Modulo(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} % {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("MOD", self.a, self.b, self.reg_save)

    class BitShiftLeft(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} << {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("BSL", self.a, self.b, self.reg_save)

    class BitShiftRight(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} >> {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("BSR", self.a, self.b, self.reg_save)

    class Or(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} | {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("OR", self.a, self.b, self.reg_save)

    class And(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} & {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("AND", self.a, self.b, self.reg_save)

    class Xor(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} ^ {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("XOR", self.a, self.b, self.reg_save)

    class Not(Instruction):
        def __init__(self, a: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = !{self.a.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("NOT", self.a, None, self.reg_save)

    class Equals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} == {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("EQ", self.a, self.b, self.reg_save)

    class NotEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} != {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("NEQ", self.a, self.b, self.reg_save)

    class GreaterThan(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} > {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("GRT", self.a, self.b, self.reg_save)

    class LessThan(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} < {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("LESS", self.a, self.b, self.reg_save)

    class GreaterThanEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} >= {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("GRTEQ", self.a, self.b, self.reg_save)

    class LessThanEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} <= {self.b.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("LESSEQ", self.a, self.b, self.reg_save)

    class MemoryWrite(Instruction):
        def __init__(self, addr: Parameter, addr_offset: int, value: Parameter):
            self.addr = addr
            self.addr_offset = addr_offset
            self.value = value

        def printInfo(self):
            print(f"    {format_memory_addr(self.addr.getInfo(), self.addr_offset)} = {self.value.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("SAVE", self.value, self.addr, ValueParameter(self.addr_offset))

    class MemRead(Instruction):
        def __init__(self, addr: Parameter, addr_offset: int, reg_save: RegisterParameter):
            self.addr = addr
            self.addr_offset = addr_offset
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {format_memory_addr(self.addr.getInfo(), self.addr_offset)}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("LOAD", ValueParameter(self.addr_offset), self.addr, self.reg_save)

    class Mov(Instruction):
        def __init__(self, value: Parameter, reg_save: RegisterParameter):
            self.value = value
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.value.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("MOV", self.value, None, self.reg_save)

    class Jump(Instruction):
        def __init__(self, dest: Parameter, cond: Optional[Parameter]):
            self.dest = dest
            self.cond = cond

        def printInfo(self):
            if self.cond is None:
                print(f"    JUMP TO {self.dest.getInfo()}")
            else:
                print(f"    JUMP TO {self.dest.getInfo()} IF {self.cond.getInfo()} == 1")

        def intoRawAssembly(self) -> str:
            cond = self.cond
            if cond is None:
                cond = ValueParameter(1)
            return generate_raw_assembly("JMP", self.dest, cond, None)

    class Push(Instruction):
        def __init__(self, val: Parameter):
            self.val = val

        def printInfo(self):
            print(f"    PUSH {self.val.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("PUSH", self.val, None, None)

    class Pop(Instruction):
        def __init__(self, reg: RegisterParameter):
            self.reg = reg

        def printInfo(self):
            print(f"    POP {self.reg.getInfo()}")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("POP", None, None, self.reg)

    class Label(Instruction):
        def __init__(self, label_name: str):
            self.label_name = label_name

        def printInfo(self):
            print(f"{self.label_name}:")

        def intoRawAssembly(self) -> str:
            return f"label {self.label_name}\n"

    class Halt(Instruction):
        def __init__(self):
            pass

        def printInfo(self):
            print(f"    HALT")

        def intoRawAssembly(self) -> str:
            return generate_raw_assembly("HLT", None, None, None)
