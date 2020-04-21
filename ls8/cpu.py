"""CPU functionality."""

import sys


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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            # self.trace()
            self.ir = self.ram_read(self.pc)  # address 0
            operand_a = self.ram_read(self.pc + 1)  # address 1   # R0
            operand_b = self.ram_read(self.pc + 2)  # address 2   # 8

            # print("self.ir", bin(self.ir))
            # print("op a", operand_a)
            # print("op b", operand_b)

            # LDI
            # print("bin if : ", self.ir)
            if bin(self.ir) == bin(0b10000010):
                # print("register[0]: ", int(self.reg[self.pc]))
                self.reg[self.pc] = operand_b
                # print("print", operand_a)
                # print("register[0]: ", self.reg[self.pc])
                self.pc += 3
                # print(self.reg[self.pc])
                # print(int(self.reg[self.pc]))

            # PRN
            elif bin(self.ir) == bin(0b01000111):
                print("Register[0]!!!: ", self.reg[operand_a])
                self.pc += 2

            # HLT
            elif bin(self.ir) == bin(0b00000001):
                print("EXITING!")
                running = False
                exit()

            else:
                print("Unknown Instruction")
