"""
Stages.py
Author: Trey Franklin
Created: March 25, 2017
Modified: March 25, 2017

Home to all the stages of the pipeline.. maybe
"""
from control import Control
from Instruction import create_sized_binary_num, decode_signed_binary_number


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
        next_stage.receive_instruction(self.fetch_instruction(), self.program_counter + 4)
        # TODO: this probably needs to update the program counter too, right?
        # TODO: should there be a method that's called when the outcome of the branch has been determined?


class Decode(object):
    def __init__(self, register_file, next_stage):
        """
        Initialized to none because this wouldn't be populated until the
        Fetch stage had fetched an instruction and sent it to the decode stage
        :param register_file: list representing the values in all of the registers. SHOULD BE 32 BIT VALUES
        """
        self._instruction = None
        self.register_file = register_file
        self.read_reg_1 = None
        self.read_reg_2 = None
        self.write_register = None
        self.sign_extended_immediate = None
        self._control = Control()
        self.next_stage = next_stage
        self._program_counter_value = None
        self.jump_address = None

    def receive_instruction(self, instruction, program_counter_value):
        """
        What happens when we receive an instruction?
        :param instruction: Instruction object
        :param program_counter_value: Value of the program counter to pass to the execute stage
        :return:
        """
        self._instruction = instruction
        self._program_counter_value = program_counter_value
        self.update_control()
        self.read_reg_1 = instruction.rs
        self.read_reg_2 = instruction.rt
        self.update_write_register()
        self.sign_extend_immediate_field()
        self.calculate_jump_address()

        self.send_data_to_next_stage()

    def send_data_to_next_stage(self):
        """
        Sends the relevant data and control information to the next stage by calling two methods of the next stage
        :return:
        """
        self.next_stage.receive_data(self.register_file[int(self.read_reg_1, 2)],
                                     self.register_file[int(self.read_reg_2, 2)], self.sign_extended_immediate,
                                     self._program_counter_value, self.jump_address)  # because this line passes through the decode stage

        self.next_stage.receive_control_information(self._control.ALUOp, self._instruction.function_field,
                                                    self._instruction.opcode, self._control.ALUSrc,
                                                    self._control.MemWrite, self._control.MemtoReg,
                                                    self._control.MemRead, self._control.Branch, self._control.jump)

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
            self.sign_extended_immediate = create_sized_binary_num(
                decode_signed_binary_number(self._instruction.immediate, 16), 32)

    def calculate_jump_address(self):
        """
        This happens in the decode stage, and is done by shifting the bottom 26 bits of the instruction (address) left 2
        and then concatenating the top four bits of the program counter to this to create a 32 bit address to go to
        :return: None
        """
        address = create_sized_binary_num(decode_signed_binary_number(self._instruction.binary_version()[:26], 26) << 2, 28)  # shift bottom 26 bits left by two
        self.jump_address = create_sized_binary_num(self._program_counter_value, 32)[28:32] + address # May not be right maths


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
        """
        Create all of the class attributes and initialize them to None.
        """
        # Control lines
        self._Branch = None
        self._MemRead = None
        self._MemtoReg = None
        self.ALUOp = None
        self._MemWrite = None
        self.ALUSrc = None
        self._jump = None

        # Data
        self.function_code = None
        self.opcode = None
        self.immediate = None
        self.read_data1 = None
        self.read_data2 = None
        self._program_counter_value = None
        self._jump_address = None

        # internal control lines
        self.operation = None
        self.branch_equal = False
        self.branch_not_equal = False

        # internal data
        self.alu_input_1 = None
        self.alu_input_2 = None
        self.alu_output = None
        self.alu_branch = None

        self.branch_address = None

    def receive_data(self, data1, data2, immediate, pc_value, jump_address):
        """
        Data information has been received, update the relevant class attributes
        :param data1: value from register1
        :param data2: value from register2
        :param immediate: sign-extended immediate
        :param pc_value: value of the program counter
        :return:
        """
        self.read_data1 = data1
        self.read_data2 = data2
        self.immediate = immediate
        self._program_counter_value = pc_value
        self._jump_address = jump_address

    def receive_control_information(self, ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead, Branch, jump):
        """
        Control information has been received, so update those class attributes next
        :param ALUOp: 2-bit alu control selection
        :param function_field: used for R-Format instructions to tell the ALU what to do
        :param opcode: opcode of the instruction, needed because of addi, andi immediate instructions
        :param ALUSrc: determines where the data for the second argument into the ALU will come from
        :param MemWrite: passed through to mem stage
        :param MemtoReg: passed through to mem stage
        :param MemRead:  passed through to mem stage
        :param Branch: passed through to mem stage
        :return:
        """
        self.ALUOp = ALUOp
        self.function_code = function_field
        self.opcode = opcode
        self.ALUSrc = ALUSrc
        self._MemWrite = MemWrite
        self._MemtoReg = MemtoReg
        self._MemRead = MemRead
        self._Branch = Branch
        self.process_alu_control()
        self.set_alu_inputs()
        self.execute_alu_operation()
        self.calculate_branch_address()

    def process_alu_control(self):
        """
        Method to process the ALU control information and set the corresponding operation for the ALU to perform.
        :return: None
        """
        if self.ALUOp == 0b00:  # LW/SW
            self.operation = 0b0010  # add

        elif self.ALUOp == 0b01:  # branch
            self.operation = 0b0110  # subtract
            if decode_signed_binary_number(self.opcode, 6) == 4:  # branch if equal
                self.branch_equal = True
            elif decode_signed_binary_number(self.opcode, 6) == 5:  # branch if not equal
                self.branch_not_equal = True
            else:
                raise Exception("(Execute): "
                                "Invalid ALUOp and opcode combination! (branching ALUOp, but opcode != beq or bne")

        elif self.ALUOp == 0b10:  # r-type instruction
            funct_int = decode_signed_binary_number(self.function_code, 6, True)
            if funct_int == 32:  # addition
                self.operation = 0b0010

            elif funct_int == 36:  # logical AND
                self.operation = 0b0000

            elif funct_int == 26:  # division
                self.operation = 0b0011

            elif funct_int == 37:  # logical OR
                self.operation = 0b0001

            elif funct_int == 24:  # multiplication
                self.operation = 0b0100

            elif funct_int == 42:  # set on less than
                self.operation = 0b0111

            elif funct_int == 34:  # subtraction
                self.operation = 0b0110

            elif funct_int == 38:  # exclusive OR
                self.operation = 0b1000
            else:
                raise Exception("(Execute): Invalid ALUOp and function field! "
                                "(Couldn't decode correct ALU function from funct field!)")

        elif self.ALUOp == 0b11:  # immediate function..
            if decode_signed_binary_number(self.opcode, 6, True) == 8:  # ADD Immediate
                self.operation = 0b0010
            elif decode_signed_binary_number(self.opcode, 6, True) == 12:  # AND Immediate
                self.operation = 0b0000
            else:
                raise Exception("(Execute): Error! Invalid immediate function and opcode combination!")

        else:
            raise Exception("(Execute): Invalid ALUOp!")

    def set_alu_inputs(self):
        """
        Sets the values of the two data inputs into the ALU. alu_input_1 will always be the data read from the first
        register in the register file, and alu_input_2 will either be the data from the second register, or the
        immediate, depending on the value of ALUSrc.
        :return: None
        """
        if len(self.read_data1) != 32:
            raise Exception("(Execute): data from register 1 isn't 32 bits1")

        self.alu_input_1 = decode_signed_binary_number(self.read_data1, 32)  # expecting 32 bit values!

        if self.ALUSrc:
            self.alu_input_2 = decode_signed_binary_number(self.immediate, 32)

        else:
            self.alu_input_2 = decode_signed_binary_number(self.read_data2, 32)

    def execute_alu_operation(self):
        """
        Perform the specified ALU Operation and set alu_output, alu_branch accordingly
        :return: None
        """
        if self.operation == 0b0000:  # AND
            self.alu_output = self.alu_input_1 & self.alu_input_2

        elif self.operation == 0b0001: # OR
            self.alu_output = self.alu_input_1 | self.alu_input_2

        elif self.operation == 0b0010:  # ADD
            self.alu_output = self.alu_input_1 + self.alu_input_2

        elif self.operation == 0b0011:  # DIV
            self.alu_output = self.alu_input_1 / self.alu_input_2

        elif self.operation == 0b0100:  # MULT
            self.alu_output = self.alu_input_1 * self.alu_input_2

        elif self.operation == 0b0110:  # SUB
            self.alu_output = self.alu_input_1 - self.alu_input_2
            if self.branch_not_equal:
                if self.alu_output == 0:
                    self.alu_branch = False
                else:
                    self.alu_branch = True

            elif self.branch_equal:
                if self.alu_output == 0:
                    self.alu_branch = True
                else:
                    self.alu_branch = False

        elif self.operation == 0b0111:  # set on less than
            if self.alu_input_1 < self.alu_input_2:  # TODO: Is this necessary?
                self.alu_output = 1
            else:
                self.alu_output = 0

        elif self.operation == 0b1000:  # XOR
            self.alu_output = self.alu_input_1 ^ self.alu_input_2

        elif self.operation == 0b1100:  # NOR
            self.alu_output = not (self.alu_input_1 | self.alu_input_2)  # This probably actually doesn't work

        else:
            raise Exception("(Execute): Unsupported ALU operation!")

        # convert output to 32-bit binary number
        self.alu_output = create_sized_binary_num(self.alu_output, 32)

    def calculate_branch_address(self):
        """
        Calculate the address the branch would take if we do branch
        :return: None
        """
        if self.immediate:
            self.branch_address = create_sized_binary_num(self._program_counter_value +
                                                          (decode_signed_binary_number(self.immediate, 32) << 2), 32)
            if len(self.branch_address) > 32:
                self.branch_address = self.branch_address[:32]
        elif self.branch_equal or self.branch_not_equal:
            raise Exception("(Execute): Attempted to branch without a value in the immediate field.")

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
