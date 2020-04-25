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
        self.pc = 0
      # * Program Counter, address of the currently executing instruction.  what do i initialize this to?
        # * Instruction Register, contains a copy of the currently executing instruction
        self.ir = self.ram[self.pc]
        # Establish a lookup dictionary for the flags after CMP function can utilize value lookup from self for JNE and JEQ jumps
        self.flags = {}
        self.address = 0

        # Stack Pointer
        self.sp = 7  # Used to refer to Register 7
        # Starting ram index per spec, 244
        self.sp_mem_index = 0xF4
        # Register 7        assigned to STARTING memory[index] 244(0xF4) for STACK processes PUSH/POP
        self.reg[self.sp] = self.ram[self.sp_mem_index]

        # Program Machine Codes  #this could be improved.  Probably not ideal to have the Machine codes.
        self.OP_LDI = 0b10000010
        self.OP_PUSH = 0b01000101
        self.OP_POP = 0b01000110
        self.OP_CALL = 0b01010000
        self.OP_RET = 0b00010001
        self.OP_PRN = 0b01000111
        self.OP_ADD = 0b10100000
        self.OP_MUL = 0b10100010
        self.OP_HLT = 0b00000001
        self.OP_CMP = 0b10100111
        self.OP_JMP = 0b01010100
        self.OP_JNE = 0b01010110
        self.OP_JEQ = 0b01010101

        # Dispatch Table - Beautifying RUN  # likely a better way to dynamically do this.
        self.dispatchtable = {}
        self.dispatchtable[self.OP_LDI] = self.handle_LDI
        self.dispatchtable[self.OP_PUSH] = self.handle_PUSH
        self.dispatchtable[self.OP_POP] = self.handle_POP
        self.dispatchtable[self.OP_CALL] = self.handle_CALL
        self.dispatchtable[self.OP_RET] = self.handle_RET
        self.dispatchtable[self.OP_PRN] = self.handle_PRN
        self.dispatchtable[self.OP_ADD] = self.handle_ADD
        self.dispatchtable[self.OP_MUL] = self.handle_MUL
        self.dispatchtable[self.OP_CMP] = self.handle_CMP
        self.dispatchtable[self.OP_JMP] = self.handle_JMP
        self.dispatchtable[self.OP_JNE] = self.handle_JNE
        self.dispatchtable[self.OP_JEQ] = self.handle_JEQ
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

    # The computer's ALU is responsible for processing mathematical calculations.
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        a_value = self.reg[reg_a]
        b_value = self.reg[reg_b]
        if op == "ADD":
            # v1 that simply assigns
            self.reg[reg_a] += self.reg[reg_b]

            # v2.  manages the bounds of the result to maintain the result under 8 bits (i.e. 00000000)
            # self.reg[reg_a] = (self.reg[reg_a] + self.reg[reg_b]) & 0xFF

        elif op == "MUL":
            # print(f"multiplying {self.reg[reg_a]} x {self.reg[reg_b]} which equals {self.reg[reg_a] * self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]

        # self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b]) & 0xFF
        # establish compare function according to guidelines
        # Compare through an else-if chain will set the flags in established dictionary to determine jumps for JNE and JEQ following instructions
        # Store value in dictionary keys to be checked for later if E= 1 then two values in reg a and b compared are established to be equal etc. L is for value compare of less than truth value of 1 or 0 and G for greater than comparision.
        elif op == "CMP":
            if a_value == b_value:
                self.flags['E'] = 1
            else:
                self.flags['E'] = 0
            if a_value < b_value:
                self.flags['L'] = 1
            else:
                self.flags['L'] = 0
            if a_value > b_value:
                self.flags['G'] = 1
            else:
                self.flags['G'] = 0

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

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

    def handle_PUSH(self, increment, opa):
        self.sp_mem_index -= 1
        self.ram[self.sp_mem_index] = self.reg[opa]

        self.pc += increment

    def handle_POP(self, increment, opa):
        self.reg[opa] = self.ram[self.sp_mem_index]

        self.sp_mem_index += 1
        self.pc += increment

    def handle_CALL(self, increment, opa):
        next_instruct = (self.pc + increment)

        # decrement memory stack location, add next instruct to stack
        self.sp_mem_index -= 1
        self.ram[self.sp_mem_index] = next_instruct
        # print(self.ram[self.sp_mem_index], "EHFIELF")
        # reassign self.pc to value in given register
        self.pc = self.reg[opa]

    def handle_RET(self):
        # pop return address from top of stack
        ret_address = self.ram[self.sp_mem_index]
        self.sp_mem_index += 1

        self.pc = ret_address

    def handle_PRN(self, increment, opa=None):
        # print(f"Register[{opa}]!!!: ", hex(self.reg[opa]).lstrip("0x"))
        print(f"Register[{opa}]!!!: ", self.reg[opa])
        self.pc += increment

    def handle_MUL(self, increment, opa=None, opb=None):
        self.alu("MUL", opa, opb)
        self.pc += increment

    def handle_ADD(self, increment, opa=None, opb=None):
        self.alu("ADD", opa, opb)
        self.pc += increment

    def handle_CMP(self, increment, opa=None, opb=None):
        self.alu("CMP", opa, opb)
        self.pc += increment

    def handle_JMP(self, increment, opa=None):
        self.pc = self.reg[opa]
        self.pc += increment

    def handle_JEQ(self, increment, opa=None):
        if self.flags['E'] == 1:
            self.pc = self.reg[opa]
        else:
            self.pc += increment

    def handle_JNE(self, increment, opa=None):
        if self.flags['E'] == 0:
            self.pc = self.reg[opa]
        else:
            self.pc += increment

    def handle_HLT(self):
        sys.exit("EXITING!")

    # ************** END Beauty Functions **************

    def run(self):

        while True:
            self.trace()
            self.ir = self.ram_read(self.pc)  # address 0
            operand_a = self.ram_read(self.pc + 1)  # address 1   # R0
            operand_b = self.ram_read(self.pc + 2)  # address 2   # 8
            # Track the instruction length to increment self.pc dynamically.
            # 1. `AND` the Instruction against binary isolator
            #   Binary Isolator uses a 1 in the location of what you want to keep
            # i.e. if instruction or self.ir in this case is 01000111, the 01 at the beginning of the binary value tells us how many arguments and operand values follow in the instruction file(see .ls8 file). So we would use 11000000 then do (01000111 & 11000000) to get the result 0f 01000000 then do step 2
            # 2. `>>` Right Shift the result of the `&` operation.
            # 3. Increment 1 to move to the NEXT instruction
            len_instruct = ((self.ir & 11000000) >> 6) + 1
            # Checking for jump instructions JMP JEQ JNE
            # jump_instruct = [JMP, JNE, JEQ]
            # Branchtable/Dispatchtable example version...?  Not working as expected.

            # if self.ir in jump_instruct:
            #     self.dispatchtable[self.ir](operand_a, operand_a)
            if len_instruct == 3:
                self.dispatchtable[self.ir](len_instruct, operand_a, operand_b)
            elif len_instruct == 2:
                self.dispatchtable[self.ir](len_instruct, operand_a)
            elif len_instruct == 1:
                self.dispatchtable[self.ir](self)
            else:
                print("Unknown Instruction")
