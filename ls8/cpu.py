"""CPU functionality."""

import sys


OP_LDI = 0b10000010
OP_PRN = 0b01000111
OP_MUL = 0b10100010
OP_HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Step 1: Add the constructor to `cpu.py`
        # Add list properties to the `CPU` class to hold 256 bytes of memory and 8 general-purpose registers.
        # 8 bytes that will each have an 8 bit value.  00000000 for a max of 8 registers
        self.reg = [0] * 8
        # since each 0 in self.reg is a bit and each self.reg contains eight 0, that is equal to 1 byte.  so the ram should only be permitted a max of 256 bytes by doing self.reg * 256???
        self.ram = [0] * 256
        # Internal Registers
        self.pc = 0  # * Program Counter, address of the currently executing instruction.  what do i initialize this to?
        # * Instruction Register, contains a copy of the currently executing instruction
        self.ir = self.ram[self.pc]
        # Dispatch Table - Beautifying RUN:
        self.dispatchtable = {}
        self.dispatchtable[OP_LDI] = self.handle_LDI
        self.dispatchtable[OP_PRN] = self.handle_PRN
        self.dispatchtable[OP_MUL] = self.handle_MUL
        self.dispatchtable[OP_HLT] = self.handle_HLT

    # In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
    # the `CPU` object.

    # `ram_read()` should accept the address to read and return the value stored
    # there.

    # `ram_write()` should accept a value to write, and the address to write it to.

    # Inside the CPU, there are two internal registers used for memory operations:
    # the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). The
    # MAR contains the address that is being read or written to. The MDR contains
    # the data that was read or the data to write. You don't need to add the MAR or
    # MDR to your `CPU` class, but they would make handy parameter names for
    # `ram_read()` and `ram_write()`, if you wanted.

    # MAR is Memory Address Register; holds the memory address we're reading or writing.
    # MDR is Memory Data Register, holds the value to write or the value just read.

    # ram_read()

    def ram_read(self, MAR):
        return self.ram[MAR]

    # ram_write()
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program_file):
        """Load a program into memory."""
        address = 0

        with open(program_file) as pf:
            for line in pf:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                self.ram[address] = int(line, base=2)
                # print(type(int(line, base=2)))
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            # print(f"multiplying {self.reg[reg_a]} x {self.reg[reg_b]} which equals {self.reg[reg_a] * self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ************** Beauty OP Functions **************
    def handle_LDI(self, increment, opa, opb):
        self.reg[opa] = opb
        self.pc += increment

    def handle_PRN(self, increment, opa):
        print("Register[0]!!!: ", hex(self.reg[opa]).lstrip("0x"))
        self.pc += increment

    def handle_MUL(self, increment, opa, opb):
        self.alu("MUL", opa, opb)
        self.pc += increment

    def handle_HLT(self):
        sys.exit("EXITING!")

    # ************** END Beauty Functions **************

    def run(self):
        """Run the CPU."""

        while True:
            # self.trace()
            self.ir = self.ram_read(self.pc)  # address 0
            operand_a = self.ram_read(self.pc + 1)  # address 1   # R0
            operand_b = self.ram_read(self.pc + 2)  # address 2   # 8

            # track the instruction length to increment self.pc dynamically. Binary isolator of length 6 trailing 0's from 11 will allow us to then shift the two leading values xx000000 and add 1  to the length of instruction to reach the position of the next program within memory as lentgh of instruction is 1 less than the length to the next program command.
            len_instruct = ((self.ir & 11000000) >> 6) + 1
            # print("length of instructions: ", len_instruct)

            # LDI
            if self.ir == OP_LDI:
                self.dispatchtable[self.ir](len_instruct, operand_a, operand_b)

            # PRN
            elif self.ir == OP_PRN:
                self.dispatchtable[OP_PRN](len_instruct, operand_a)

            # MUL
            elif self.ir == OP_MUL:
                self.dispatchtable[self.ir](len_instruct, operand_a, operand_b)

            # HLT
            elif self.ir == OP_HLT:
                self.dispatchtable[OP_HLT]()

            else:
                print("Unknown Instruction")
