"""
Interface.py
Created: March 25, 2017
Author: Trey Franklin

Creates a datapath from the pipeline components and interfaces with it.
Very much not working currently.
"""

from Stages import Fetch, Decode, Execute, Memory, WriteBack


class PipelineInterface(object):
    def __init__(self, instruction_list, starting_pc_address, register_memory, data_mem):
        """
        Creates the interface to the pipeline.
        :param instruction_list: list of Instruction objects in the order they should appear in instruction memory
        :param starting_pc_address: integer starting address for the program counter. This will also be the base
        address of instruction memory
        :param register_memory: list representing register memory, since the registers are just reg0,reg1, etc
        :param data_mem: dictionary representing data memory
        """
        self.fetch = Fetch(instruction_list, starting_pc_address)

        self.write_back = WriteBack(fetch_stage=self.fetch)
        self.memory = Memory(data_mem, self.write_back)
        self.execute = Execute(self.memory)
        self.decode = Decode(register_memory, self.execute)
        self.write_back.decode_stage = self.decode

    def trigger_clock_cycle(self):
        """
        For single-cycle, we really only do something useful in the fetch.on_rising_clock. It will call a method of the
        next stage that will do what that stage needs to and then call the next stage, etc
        In pipelined execution, these would be used because Fetch would fetch the instruction, place it in the
        intermediate register, and then return back to here, where decode.on_rising_clock would be called.
        :return:
        """
        self.fetch.on_rising_clock(self.decode)
        self.decode.on_rising_clock()
        self.execute.on_rising_clock()
        self.memory.on_rising_clock()
        self.write_back.on_rising_clock()

    def retrieve_register_list(self):
        """
        Helper method to return the current register file for comparing that the instruction was written back
        successfully
        :return: list representing register file
        """
        return self.decode.register_file

    def retrieve_data_memory(self):
        """
        Helper method to return the current data memory dictionary to help ensure that the data was written to the
        correct place
        :return: memory dictionary
        """
        return self.memory.memory

    def retrieve_current_pc_address(self):
        """
        Helper method to retrieve the current value of the program counter from the fetch stage.
        :return: int (probably)
        """
        return self.fetch.program_counter

    def retrive_instruction_name(self):
        return self.decode.instruction.asm_version()
