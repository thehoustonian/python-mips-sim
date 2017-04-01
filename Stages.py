"""
Stages.py
Author: Trey Franklin
Created: March 25, 2017
Modified: March 25, 2017

Home to all the stages of the pipeline.. maybe
"""


class Fetch:
    def __init__(self, instruction_list, starting_address):
        """
        Creates the Fetch stage of the pipeline with the PC set to starting address, and instruction list
        being the Instruction Objects (in order) that represent the program.
        :param instruction_list: list of Instruction objects that will compose instruction memory
        :param starting_address: starting address of the program counter, should be noted that this will be the address
        that the first instruction is added to, and following ones will be starting_address + 4, +8, etc.
        """
        if len(instruction_list) == 0:
            raise Exception("Instruction list must have at least one instruction present!")

        self.program_counter = int(starting_address)  # initialize the program counter to the starting address
        self.instruction_memory = {}  # Use a dictionary as the representation for instruction memory

        self.setup_instruction_memory(instruction_list)
        self._i_mem_keys = sorted(self.instruction_memory.keys())  # for checking if the address of the PC is valid

    def setup_instruction_memory(self, instruction_list):
        i = 0
        for instruction in instruction_list:
            self.instruction_memory[self.program_counter + i] = instruction
            i += 4

    def fetch_instruction(self):
        """
        Fetches the instruction at the current PC address from instruction memory,
        and returns the instruction. If the PC is at an invalid address, an Exception is raised.
        :return: Instruction object
        """
        if self.program_counter not in self._i_mem_keys:
            raise Exception("Invalid Instruction Address!")

        return self.instruction_memory[self.program_counter]  # get the Instruction

    def update_program_counter(self, new_address):
        """
        Updates the program counter to the new address
        :param new_address: new value of the program counter (STRING)
        :return:
        """
        if new_address % 4 != 0:  # Have to use whole word addressing. Sorry
            raise Exception("Invalid Program Counter Value!")
        else:
            self.program_counter = new_address

    def increment_program_counter(self):
        """
        Increments the program counter by adding four to the address
        :return: None
        """
        self.update_program_counter(self.program_counter + 4)


class Decode:
    def __init__(self):
        print("Not Implemented")


class Execute:
    def __init__(self):
        print("Not Implemented")


class Memory:
    def __init__(self):
        print("Not Implemented")


class WriteBack:
    def __init__(self):
        print("Not Implemented")