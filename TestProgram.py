"""
TestProgram.py

Demonstration program for my pipeline simulator

Created: 3/25/17
Modified: 3/25/17
Author: Trey Franklin
"""

from PipelineInterface import PipelineInterface
from python_test_program import python_test_program
from Instruction import Instruction, create_sized_binary_num, decode_signed_binary_number, decode_asm_register
from time import sleep

print("This program will execute the provided test program for my Pipeline Simulator.")
print("Currently, the pipeline is single-cycle, with no hazard detection, forwaring, or pipelining")
print("Created by Trey Franklin")
print("-----------------------------------------------------------------------")
sleep(2)

print("Creating register file..")
register_file = [create_sized_binary_num(0, 32) for i in range(0, 32)]  # initialize all registers to zero
register_file[decode_asm_register('v0')] = create_sized_binary_num(0x0040, 32)
register_file[decode_asm_register('v1')] = create_sized_binary_num(0x1010, 32)
register_file[decode_asm_register('s2')] = create_sized_binary_num(0x000F, 32)
register_file[decode_asm_register('s3')] = create_sized_binary_num(0x00F0, 32)
register_file[decode_asm_register('t0')] = create_sized_binary_num(0x0000, 32)
register_file[decode_asm_register('a0')] = create_sized_binary_num(0x0010, 32)
register_file[decode_asm_register('a1')] = create_sized_binary_num(0x0005, 32)

print("Creating data memory..")
data_memory_addresses = [create_sized_binary_num(i, 32) for i in range(0, 512, 4)]  # word addressing (increment by 4)
data_memory = {}
for i in data_memory_addresses:
    data_memory[i] = create_sized_binary_num(0, 32)  # initialize valid memory addresses to zero

data_memory[create_sized_binary_num(0x0010, 32)] = create_sized_binary_num(0x0101, 32)
data_memory[create_sized_binary_num(0x0010 + 4, 32)] = create_sized_binary_num(0x0110, 32)
data_memory[create_sized_binary_num(0x0010 + 8, 32)] = create_sized_binary_num(0x0011, 32)
data_memory[create_sized_binary_num(0x0010 + 12, 32)] = create_sized_binary_num(0x00F0, 32)
data_memory[create_sized_binary_num(0x0010 + 16, 32)] = create_sized_binary_num(0x00FF, 32)

print("Creating Instruction Memory..")
start_addr = 0
var_exit = '14'
var_else = '4'

var_end = '20'
var_loop = '6'

instruction_memory = [Instruction('addi', '$t7', '$zero', '4'),      # 0
                      Instruction('addi', '$t6', '$zero', '32512'),  # 4  Changed to 0x7F00 b/c of sign-extension
                      Instruction('addi', '$t5', '$zero', '8'),      # 8
                      Instruction('addi', '$t3', '$zero', '256'),    # 12
                      Instruction('addi', '$t1', '$zero', '1'),      # 16
                      Instruction('addi', '$t8', '$zero', '255'),    # 20

                      Instruction('slt', '$t2', '$a1', '$t1'),       # 24 LOOP
                      Instruction('beq', '$t2', '$t1', var_exit),    # 28
                      Instruction('sub', '$a1', '$a1', '$t1'),       # 32
                      Instruction('lw', '$t0', '$a0', '0'),          # 36
                      Instruction('slt', '$t4', '$t3', '$t0'),       # 40
                      Instruction('beq', '$t4', '$zero', var_else),  # 44
                      Instruction('div', '$v0', '$v0', '$t5'),       # 48
                      Instruction('or', '$v1', '$v1', '$v0'),        # 52
                      Instruction('sw', '$t6', '$a0', '0'),          # 56
                      Instruction('j', var_end),                     # 60
                      Instruction('mult', '$s2', '$s2', '$t7'),      # 64 ELSE
                      Instruction('xor', '$s3', '$s3', '$s2'),       # 68
                      Instruction('sw', '$t8', '$a0', '0'),          # 72
                      Instruction('j', var_end),                     # 76

                      Instruction('addi', '$a0', '$a0', '4'),        # 80 END
                      Instruction('j', var_loop),                    # 84

                      Instruction('addi', '$t8', '$zero', '0')]  # 88  EXIT

print("Creating pipeline with created values for instruction memory, pc address, register file, and data memory.")
interface = PipelineInterface(instruction_memory, start_addr, register_file, data_memory)

print("Starting Program Execution... *crosses fingers*")
print("-----------------------------------------------------------------------")

clocks = 0
while True:
    try:
        interface.trigger_clock_cycle()
        print("Instruction: ", interface.retrive_instruction_name())
        # print("PC: ", interface.retrieve_current_pc_address())
        clocks += 1
        print("Clock Cycle: ", clocks)
        print("\n")

    except Exception as e:
        if "Invalid Instruction Address" in str(e):
            break
        else:
            raise Exception(str(e))

print("-----------------------------------------------------------------------")
print("Execution completed in " + str(clocks) + " clock cycles.")
print("-----------------------------------------------------------------------\n\n")

print("Running Python version of program for comparison.")
print("-----------------------------------------------------------------------\n\n")

results = python_test_program()

print("-----------------------------------------------------------------------")
print("Test completed, comparing values.\n")

current_reg_memory = interface.retrieve_register_list()
current_data_memory = interface.retrieve_data_memory()

print("-reg-|-Expected--|-----Actual--")
print(" v0  |-----" + str(results[1]) + "-----|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('v0')], 32)))
print(" v1  |-----" + str(results[2]) + "--|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('v1')], 32)))
print(" s2  |-----" + str(results[3]) + "---|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('s2')], 32)))
print(" s3  |-----" + str(results[4]) + "--|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('s3')], 32)))
print(" t0  |-----" + str(results[5]) + "---|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('t0')], 32)))
print(" a0  |-----" + str(results[6]) + "----|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('a0')], 32)))
print(" a1  |-----" + str(results[7]) + "-----|-----" +
      str(decode_signed_binary_number(current_reg_memory[decode_asm_register('a1')], 32)))
print("-----------------------------------------\n")

print("Data Memory:")
print("Location |---Expected---|---Actual---")
print("---16--- |------" + str(decode_signed_binary_number(results[0][16], 32)) + "---|-----" +
      str(decode_signed_binary_number(current_data_memory[create_sized_binary_num(16, 32)], 32)))
print("---20--- |------" + str(decode_signed_binary_number(results[0][20], 32)) + "---|-----" +
      str(decode_signed_binary_number(current_data_memory[create_sized_binary_num(20, 32)], 32)))
print("---24--- |------" + str(decode_signed_binary_number(results[0][24], 32)) + "-----|-----" +
      str(decode_signed_binary_number(current_data_memory[create_sized_binary_num(24, 32)], 32)))
print("---28--- |------" + str(decode_signed_binary_number(results[0][28], 32)) + "-----|-----" +
      str(decode_signed_binary_number(current_data_memory[create_sized_binary_num(28, 32)], 32)))
print("---32--- |------" + str(decode_signed_binary_number(results[0][32], 32)) + "-----|-----" +
      str(decode_signed_binary_number(current_data_memory[create_sized_binary_num(32, 32)], 32)))
print("----------------------------------------------------------------------")
