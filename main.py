# THIS IS JUST A DEMO OF A CPU SIMULATION FOR LEARNING PURPOSES

import os, sys


memory = [0] * 64 # bytes

segments = {
    "text": 0,
    "bss": 30,
    "data": 40,
    "heap": 45, # NOT IMPLEMENTED
    "stack": 63
}

registers = {
    0: 0,
    1: -1,
    2: 0,
    3: 0
}

# byte = 8 bit / byte = range(0, 256)

def is_off(position, offset=0):
    return max(position, offset) > 64


def is_byte(value):
    return value >= 0 and value < 257

def memory_read(position):
    assert not(is_off(position))
    
    return memory[position]


def memory_write(position, byte):
    assert not(is_off(position, position))
    assert is_byte(byte)
    
    memory[position] = byte


def memory_reset():
    for i in range(64):
        memory_write(i, 0)


def text_debug_current():
    as_string = str()
    
    try:
        if memory_read(register_read(0)) == 1:
            as_string = "push # pushes onto the top of the stack"

        elif memory_read(register_read(0)) == 2:
            as_string = "pop  # pops the top of the stack"

        elif memory_read(register_read(0)) == 3:
            as_string = "add  # adds the last two operands on the stack and pushes the result"

        elif memory_read(register_read(0)) == 4:
            as_string = "dump # prints the top of the stack"

        elif memory_read(register_read(0)) == 0:
            as_string = "halt # stops the program (exit)"

        print(f"current program instruction[{hex(register_read(0))}]: {as_string}")

    except:
        return


def register_read(register):
    return registers[register]


def register_write(register, byte):
    registers[register] = byte


def registers_reset():
    register_write(0, 0)
    register_write(1, 0)
    register_write(2, 0)
    register_write(3, 0)


def registers_debug():
    print(f"PROGRAM COUNTER (PC): {register_read(0)}")
    print(f"STACK POINTER   (SP): {register_read(1)}")
    print(f"R0:                   {register_read(2)}")
    print(f"R1:                   {register_read(3)}\n")


def stack_push(byte):
    assert is_byte(byte)

    if register_read(1) < 0:
        register_write(1, 0)

    memory_write(segments["stack"] - register_read(1), byte)
    register_write(1, register_read(1) + 1)


def stack_pop(register):
    top = memory_read(segments["stack"] - register_read(1) + 1)
    register_write(register, top)
    memory_write(segments["stack"] - register_read(1) + 1, 0)
    register_write(1, register_read(1) - 1)


def stack_debug():
    for i in range(register_read(1)):
        print(f"[{hex(i)}]: {memory_read(segments['stack'] - i)}")


def alu_add():
    stack_pop(2)
    stack_pop(3)

    result = register_read(2) + register_read(3)

    stack_push(result)


def dump():
    stack_pop(2)
    sys.stdout.write(chr(register_read(2)))
    stack_push(register_read(2))


def load_program(program):
    for index, byte in enumerate(program):
        memory_write(segments["text"] + index, byte)


def program_execute_next():
    if memory_read(register_read(0)) == 1:
        register_write(0, register_read(0) + 1)
        stack_push(memory_read(register_read(0)))
        register_write(0, register_read(0) + 1)

    elif memory_read(register_read(0)) == 2:
        register_write(0, register_read(0) + 1)
        stack_pop(memory_read(register_read(0)))
        register_write(0, register_read(0) + 1)

    elif memory_read(register_read(0)) == 3:
        alu_add()
        register_write(0, register_read(0) + 1)

    elif memory_read(register_read(0)) == 4:
        dump()
        register_write(0, register_read(0) + 1)

    elif memory_read(register_read(0)) == 0:
        return False

    return True


program = [
    1, 10,
    1, 111,
    1, 108,
    1, 108,
    1, 101,
    1, 72,
    4,
    2, 2,
    4,
    2, 2,
    4,
    2, 2,
    4,
    2, 2,
    4,
    2, 2,
    4,
    2, 2,
    0
]

load_program(program)

# debug

while True:
    print("\n[cpu]\n\n[program]")
    text_debug_current()
    print("\n[registers]")
    registers_debug()
    print("\n[stack]")
    stack_debug()
    print()
    input("press enter to advance to the next. ")
    os.system("clear")

    if not(program_execute_next()):
        break

print("now it will run without debugging")

memory_reset()
registers_reset()
load_program(program)

while True:
    if not(program_execute_next()):
        break
