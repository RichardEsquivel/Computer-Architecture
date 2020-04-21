# '''
# Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.
# For example, given the following object/dictionary as input:
# {
#   "cat": "bob",
#   "dog": 23,
#   19: 18,
#   90: "fish"
# }
# Your algorithm should return 41, the sum of the values 23 and 18.
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.

# Access numeric values and add

# '''

# a = {
#     "cat": "bob",
#     "dog": 23,
#     19: 18,
#     90: "fish",
#     100: 23

# }


# def add_nums(nums):
#     str(nums[i])
#     total = sum([i for i in nums[i] if isinstance(i, int)])

#     return total


# print(add_nums(a))
# Write a program in Python that runs programs

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8

memory = [
    PRINT_BEEJ,

    SAVE_REG,    # SAVE R0,37   store 37 in R0      the opcode
    0,  # R0     operand ("argument")
    37,  # 37     operand

    PRINT_BEEJ,

    PRINT_REG,  # PRINT_REG R0
    0,  # R0

    HALT
]

register = [0] * 8   # like variables R0-R7

pc = 0  # Program Counter, the address of the current instruction
running = True

while running:
    inst = memory[pc]

    if inst == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif inst == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2

    elif inst == HALT:
        running = False

    else:
        print("Unknown instruction")
        running = False
