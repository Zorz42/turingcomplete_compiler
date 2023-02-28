from jaclang.generator.generator import RegisterParameter, Instruction, Parameter


class Instructions:
    class Noop(Instruction):
        def printInfo(self):
            print("    NOOP")

    class Add(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} + {self.b.getInfo()}")

    class Subtract(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} - {self.b.getInfo()}")

    class BitShiftLeft(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} << {self.b.getInfo()}")

    class BitShiftRight(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} >> {self.b.getInfo()}")

    class Or(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} | {self.b.getInfo()}")

    class And(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} & {self.b.getInfo()}")

    class Xor(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} ^ {self.b.getInfo()}")

    class Not(Instruction):
        def __init__(self, a: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = !{self.a.getInfo()}")

    class Equals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} == {self.b.getInfo()}")

    class NotEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} != {self.b.getInfo()}")

    class GreaterThan(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} > {self.b.getInfo()}")

    class LessThan(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} < {self.b.getInfo()}")

    class GreaterThanEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} >= {self.b.getInfo()}")

    class LessThanEquals(Instruction):
        def __init__(self, a: Parameter, b: Parameter, reg_save: RegisterParameter):
            self.a = a
            self.b = b
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.a.getInfo()} <= {self.b.getInfo()}")

    class MemoryWrite(Instruction):
        def __init__(self, addr: Parameter, addr_offset: int, value: Parameter):
            self.addr = addr
            self.addr_offset = addr_offset
            self.value = value

        def printInfo(self):
            print(f"    [{self.addr.getInfo()} + {self.addr_offset}] = {self.value.getInfo()}")

    class MemRead(Instruction):
        def __init__(self, addr: Parameter, addr_offset: int, reg_save: RegisterParameter):
            self.addr = addr
            self.addr_offset = addr_offset
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = [{self.addr.getInfo()} + {self.addr_offset}]")

    class Mov(Instruction):
        def __init__(self, value: Parameter, reg_save: RegisterParameter):
            self.value = value
            self.reg_save = reg_save

        def printInfo(self):
            print(f"    {self.reg_save.getInfo()} = {self.value.getInfo()}")

    class Jump(Instruction):
        def __init__(self, dest: Parameter, cond: Parameter):
            self.dest = dest
            self.cond = cond

        def printInfo(self):
            if self.cond is None:
                print(f"    JUMP TO {self.dest.getInfo()}")
            else:
                print(f"    JUMP TO {self.dest.getInfo()} IF {self.cond.getInfo()} == 1")

    class Push(Instruction):
        def __init__(self, val: Parameter):
            self.val = val

        def printInfo(self):
            print(f"    PUSH {self.val.getInfo()}")

    class Pop(Instruction):
        def __init__(self, reg: RegisterParameter):
            self.reg = reg

        def printInfo(self):
            print(f"    POP {self.reg.getInfo()}")

    class Label(Instruction):
        def __init__(self, label_name: str):
            self.label_name = label_name

        def printInfo(self):
            print(f"{self.label_name}:")
