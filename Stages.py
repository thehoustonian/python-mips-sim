"""
Stages.py
Author: Trey Franklin
Created: March 25, 2017
Modified: March 25, 2017

Home to all the stages of the pipeline.. maybe
"""
from control import Control
from Instruction import Instruction


class Fetch(object):
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

        self._setup_instruction_memory(instruction_list)
        self._i_mem_keys = sorted(self.instruction_memory.keys())  # for checking if the address of the PC is valid

    def _setup_instruction_memory(self, instruction_list):
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

    def on_rising_clock(self, next_stage):  # TODO: add next_stage as a class attribute
        """
        Method called when the clock is on a rising edge. Sends the next instruction
        to the next stage/register in the pipeline
        :param next_stage: stage to send the instruction to
        :return: None
        """
        next_stage.receive_instruction(self.fetch_instruction())
        # TODO: this probably needs to update the program counter too, right?
        # TODO: should there be a method that's called when the outcome of the branch has been determined?


class Decode(object):
    def __init__(self, register_file, next_stage):
        """
        Initialized to none because this wouldn't be populated until the
        Fetch stage had fetched an instruction and sent it to the decode stage
        :param register_file: list representing the values in all of the registers.
        """
        self._instruction = None
        self.register_file = register_file
        self.read_reg_1 = None
        self.read_reg_2 = None
        self.write_register = None
        self.sign_extended_immediate = None
        self._control = Control()
        self.next_stage = next_stage

    def receive_instruction(self, instruction):
        """
        What happens when we receive an instruction?
        :param instruction: Instruction object
        :return:
        """
        self._instruction = instruction
        self.update_control()
        self.read_reg_1 = instruction.rs
        self.read_reg_2 = instruction.rt
        self.update_write_register()
        self.sign_extend_immediate_field()

        self.next_stage.receive_immediate(self.sign_extended_immediate)
        self.next_stage.receive_alu_op(self._control.ALUOp)
        self.next_stage.update_alu_control(self._instruction.function_field, self._instruction.opcode)
        self.next_stage.read_data(self.register_file[int(self.read_reg_1, 2)], self.register_file[int(self.read_reg_2, 2)])
        self.next_stage.receive_alu_src(self._control.ALUSrc)

    def update_control(self):
        """
        Populate all the values of the control class
        :return:
        """
        self._control.update(self._instruction.opcode)

    def update_write_register(self):
        """
        Set the value of what register to write to based on the value of the RegDst control line
        :return:
        """
        if self._control.RegDst:
            self.write_register = self._instruction.rd
        else:
            self.write_register = self._instruction.rt

    def sign_extend_immediate_field(self):
        """
        Sign extend the immediate field from 16 bits to 32 bits
        :return:
        """
        if self._instruction.immediate:
            self.sign_extended_immediate = Instruction.create_sized_binary_num(
                Instruction.decode_signed_binary_number(self._instruction.immediate, 16), 32)

    def write_to_register(self, data):
        """
        When data has been received from the writeback stage, write this to the register set by update_write_register
        :param data:
        :return:
        """
        if self.write_register:
            self.register_file[int(self.write_register, 2)] = data
        else:
            raise Exception("Trying to write to a register before the write_register destination has been set!")

    # TODO: needed for pipelined version
    def on_rising_clock(self):
        pass


class Execute:
    def __init__(self):
        print("Not Implemented")

    def read_data(self, register1, register2):
        pass

    def update_alu_control(self, funct, opcode):  # need opcode because of immediate instructions.
        pass

    def receive_alu_op(self, ALUOp):
        pass

    def receive_immediate(self, immediate):
        pass

    def receive_alu_src(self, ALUSrc):
        pass

    def on_rising_clock(self):
        pass


class Memory:
    def __init__(self):
        print("Not Implemented")

    def on_rising_clock(self):
        pass


class WriteBack:
    def __init__(self):
        print("Not Implemented")

    def on_rising_clock(self):
        pass
