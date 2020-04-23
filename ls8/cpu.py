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

        self.address = 0

        # Stack Pointer
        self.sp = 7  # Used to refer to Register 7
        # Starting ram index per spec, 244
        self.sp_mem_index = 0xF4
        # Register 7        assigned to STARTING memory[index] 244(0xF4) for STACK processes PUSH/POP
        self.reg[self.sp] = self.ram[self.sp_mem_index]

        # Program Machine Codes
        self.OP_LDI = 0b10000010
        self.OP_PUSH = 0b01000101
        self.OP_POP = 0b01000110
        self.OP_PRN = 0b01000111
        self.OP_MUL = 0b10100010
        self.OP_HLT = 0b00000001

        # Dispatch Table - Beautifying RUN:
        self.dispatchtable = {}
        self.dispatchtable[self.OP_LDI] = self.handle_LDI
        self.dispatchtable[self.OP_PUSH] = self.handle_PUSH
        self.dispatchtable[self.OP_POP] = self.handle_POP
        self.dispatchtable[self.OP_PRN] = self.handle_PRN
        self.dispatchtable[self.OP_MUL] = self.handle_MUL
        self.dispatchtable[self.OP_HLT] = self.handle_HLT

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
        with open(program_file) as pf:
            for line in pf:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                self.ram[self.address] = int(line, base=2)
                # print(type(int(line, base=2)))
                self.address += 1

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
            # v1 that simply assigns
            self.reg[reg_a] += self.reg[reg_b]

            # v2.  manages the bounds of the result to maintain the result under 8 bits (i.e. 00000000)
            # self.reg[reg_a] = (self.reg[reg_a] + self.reg[reg_b]) & 0xFF

        elif op == "MUL":
            # print(f"multiplying {self.reg[reg_a]} x {self.reg[reg_b]} which equals {self.reg[reg_a] * self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]
            # self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b]) & 0xFF
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

    # register
    [
        # pop direction
        # assign register[0-2] to be equal to memory[memoryindexinhex]
    ]

    # Memory
    [
        # push direction
        # assign memory[memoryindexinhex] to be = to something in register[0-2]
        # starting at memory[244]
    ]

    def handle_PUSH(self, increment, opa):
        self.sp_mem_index -= 1
        self.ram[self.sp_mem_index] = self.reg[opa]

        self.pc += increment

    def handle_POP(self, increment, opa):
        self.reg[opa] = self.ram[self.sp_mem_index]

        self.sp_mem_index += 1
        self.pc += increment

    def handle_PRN(self, increment, opa):
        # print(f"Register[{opa}]!!!: ", hex(self.reg[opa]).lstrip("0x"))
        print(f"Register[{opa}]!!!: ", self.reg[opa])
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

            # track the instruction length to increment self.pc dynamically.
            # 1. `AND` the Instruction against binary isolator
            #   Binary Isolator uses a 1 in the location of what you want to keep
            # i.e. if instruction or self.ir in this case is 01000111, the 01 at the beginning of the binary value tells us how many arguments and operand values follow in the instruction file(see .ls8 file). So we would use 11000000 then do (01000111 & 11000000) to get the result 0f 01000000 then do step 2
            # 2. `>>` Right Shift the result of the `&` operation.
            # 3. Increment 1 to move to the NEXT instruction
            len_instruct = ((self.ir & 11000000) >> 6) + 1

            # LDI
            if self.ir == self.OP_LDI:
                self.dispatchtable[self.OP_LDI](
                    len_instruct, operand_a, operand_b)

            # PUSH
            elif self.ir == self.OP_PUSH:
                self.dispatchtable[self.OP_PUSH](len_instruct, operand_a)

            # POP
            elif self.ir == self.OP_POP:
                self.dispatchtable[self.OP_POP](len_instruct, operand_a)

            # PRN
            elif self.ir == self.OP_PRN:
                self.dispatchtable[self.OP_PRN](len_instruct, operand_a)

            # MUL
            elif self.ir == self.OP_MUL:
                self.dispatchtable[self.OP_MUL](
                    len_instruct, operand_a, operand_b)

            # HLT
            elif self.ir == self.OP_HLT:
                self.dispatchtable[self.OP_HLT]()

            else:
                print("Unknown Instruction")
