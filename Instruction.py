"""
Instruction.py

The Instruction class == an abstract representation of a 32-bit MIPS assembly instruction

Created: 3/25/17
Author: Trey Franklin
"""


def create_sized_binary_num(decimal_num, desired_len):
    """
    Returns a string representing a binary number with a specific size (buffers with zeros to get correct len)
    Takes inspiration from:
    http://stackoverflow.com/questions/1395356/how-can-i-make-bin30-return-00011110-instead-of-0b11110

    for 2s complement processing: http://stackoverflow.com/questions/1604464/twos-complement-in-python

    :param decimal_num: decimal representation of the number
    :param desired_len: how long should the final number be? (WILL NOT TRUNCATE IF desired_len == < len(decimal_num)
    :return: binary string
    """
    if int(decimal_num) < 0:
        decimal_num = int(decimal_num) + (1 << desired_len)
    num = bin(int(decimal_num))[2:].zfill(desired_len)
    if len(num) != desired_len:
        raise Exception(
            "Error creating binary number of desired length! (did this function get a binary value instead?)")
    else:
        return num


def decode_signed_binary_number(binary_num, bit_count, force_unsigned=False):
    """
    It's nice to be able to decode the signed binary numbers too.
    :param binary_num: the string representation of the binary number
    :param bit_count: how many bits in the binary number?
    :param force_unsigned: Force this function to do an unsigned operation
    :return: integer representing the binary number
    """
    if binary_num[0] == '1' and not force_unsigned:
        return int(binary_num, 2) - (1 << bit_count)
    else:
        return int(binary_num, 2)


def decode_asm_register(register):  # TODO: This isn't best practice, remove the method from the class too.
    """
    Takes a MIPS assembly representation of a register and converts it to the corresponding register number
    :param register:
    :return:
    """
    if register == "zero":
        return 0
    elif register in ['v0', 'v1']:
        return int(register[1]) + 2
    elif register in ['a0', 'a1', 'a2', 'a3']:
        return int(register[1]) + 4
    elif register in ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']:
        return int(register[1]) + 8
    elif register in ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7']:
        return int(register[1]) + 16
    elif register in ['t8', 't9']:
        return int(register[1]) + 16
    elif register == 'gp':
        return 28
    elif register == 'sp':
        return 29
    elif register == 'fp':
        return 30
    elif register == 'ra':
        return 31
    else:
        raise Exception("Error processing a register decode")


def decode_int_reg_val(reg_num):
     return ['$zero', '$at',
            '$v0', '$v1',
            '$a0', '$a1', '$a2', '$a3',
            '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
            '$s0', '$s1','$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
            '$t8', '$t9', '$k0', '$k1',
            '$gp', '$sp', '$fp', '$ra'][reg_num]


class Instruction:
    def __init__(self, inst_name, inst_arg1, inst_arg2=None, inst_arg3=None):
        """
        Initialize the Instruction object from the passed in info
        :param inst_name: name of instruction (ADD, sub, etc)
        :param inst_arg1: first argument of the instruction (t1, s1, target, etc)
        :param inst_arg2: second arg (t2)
        :param inst_arg3: third arg (could be register, immediate, or branch target)
        """
        self.name = inst_name.lower()
        self._arg1 = inst_arg1.lower().replace("$", "") if inst_arg1 is not None else inst_arg1
        self._arg2 = inst_arg2.lower().replace("$", "") if inst_arg2 is not None else inst_arg2
        self._arg3 = inst_arg3.lower().replace("$", "") if inst_arg3 is not None else inst_arg3

        self.format = None
        self.branching = False
        self.memory_op = False
        self.binary_name = None
        self.opcode = '000000'
        self.rs = '00000'
        self.rt = '00000'
        self.rd = '00000'
        self.shift_amount = create_sized_binary_num(0, 5)
        self.function_field = '000000'
        self.immediate = '0000000000000000'
        self.address = '00000000000000000000000000'
        self.full_binary_rep = None

        self.determine_format()
        self.populate_opcode()
        self.populate_rs()
        self.populate_rt()
        self.populate_rd()
        self.populate_function_field()
        self.populate_immediate()
        self.populate_address()
        self.create_binary()

    def create_binary(self):
        if self.format == "R":
            self.full_binary_rep = "{}{}{}{}{}{}".format(self.opcode, self.rs, self.rt, self.rd, self.shift_amount,
                                                         self.function_field)
        elif self.format == "I":
            self.full_binary_rep = "{}{}{}{}".format(self.opcode, self.rs, self.rt, self.immediate)

        elif self.format == "J":
            self.full_binary_rep = "{}{}".format(self.opcode, self.address)
        else:
            raise Exception("Something broke and idk what happened in Instruction class.")

    @staticmethod
    def decode_asm_register(register):
        """
        Takes a MIPS assembly representation of a register and converts it to the corresponding register number
        :param register:
        :return:
        """
        if register == "zero":
            return 0
        elif register in ['v0', 'v1']:
            return int(register[1]) + 2
        elif register in ['a0', 'a1', 'a2', 'a3']:
            return int(register[1]) + 4
        elif register in ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']:
            return int(register[1]) + 8
        elif register in ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7']:
            return int(register[1]) + 16
        elif register in ['t8', 't9']:
            return int(register[1]) + 16
        elif register == 'gp':
            return 28
        elif register == 'sp':
            return 29
        elif register == 'fp':
            return 30
        elif register == 'ra':
            return 31
        else:
            raise Exception("Error processing a register decode")

    def determine_format(self):
        """
        determine what the format of the instruction == based on the name (R, I, or J type)
        :return:
        """
        if self.name in ['add', 'and', 'div', 'or', 'mult', 'slt', 'sub', 'xor']:
            self.format = "R"

        elif self.name in ['addi', 'andi', 'beq', 'bne', 'lw', 'sw']:
            self.format = "I"
            if self.name in ['beq', 'bne']:
                self.branching = True
            elif self.name in ['lw', 'sw']:
                self.memory_op = True

        elif self.name == 'j':
            self.format = "J"

        else:
            raise Exception("Unrecognized Instruction (Format)")

    def populate_opcode(self):
        """
        Create the opcode string
        :return:
        """
        if self.format == 'R':
            self.opcode = create_sized_binary_num(0, 6)

        elif self.format == 'I':
            if self.name == 'addi':
                self.opcode = create_sized_binary_num(8, 6)

            elif self.name == 'andi':
                self.opcode = create_sized_binary_num(12, 6)

            elif self.name == 'beq':
                self.opcode = create_sized_binary_num(4, 6)

            elif self.name == 'bne':
                self.opcode = create_sized_binary_num(5, 6)

            elif self.name == 'lw':
                self.opcode = create_sized_binary_num(35, 6)

            elif self.name == 'sw':
                self.opcode = create_sized_binary_num(43, 6)

            else:
                raise Exception("Unrecognized I-Format Instruction")

        elif self.format == 'J':
            self.opcode = create_sized_binary_num(2, 6)

        else:
            raise Exception("Unrecognized format")

        if len(self.opcode) != 6:
            raise Exception("Problem creating opcode string")

    def populate_rs(self):
        if self.format == "R" or (self.format == "I" and self.branching is False):
            self.rs = create_sized_binary_num(self.decode_asm_register(self._arg2), 5)
        elif self.format == 'I' and self.branching is True:
            self.rs = create_sized_binary_num(self.decode_asm_register(self._arg1), 5)

    def populate_rt(self):
        if self.format == "R":
            self.rt = create_sized_binary_num(self.decode_asm_register(self._arg3), 5)
        elif self.format == "I" and self.branching is False:
            self.rt = create_sized_binary_num(self.decode_asm_register(self._arg1), 5)
        elif self.format == "I" and self.branching is True:
            self.rt = create_sized_binary_num(self.decode_asm_register(self._arg2), 5)

    def populate_rd(self):
        if self.format == "R":
            self.rd = create_sized_binary_num(self.decode_asm_register(self._arg1), 5)

    def populate_function_field(self):
        if self.format == "R":
            if self.name == 'add':
                self.function_field = create_sized_binary_num(32, 6)
            elif self.name == 'and':
                self.function_field = create_sized_binary_num(36, 6)
            elif self.name == 'div':
                self.function_field = create_sized_binary_num(26, 6)
            elif self.name == 'or':
                self.function_field = create_sized_binary_num(37, 6)
            elif self.name == 'mult':
                self.function_field = create_sized_binary_num(24, 6)
            elif self.name == 'slt':
                self.function_field = create_sized_binary_num(42, 6)
            elif self.name == 'sub':
                self.function_field = create_sized_binary_num(34, 6)
            elif self.name == 'xor':
                self.function_field = create_sized_binary_num(38, 6)
            else:
                raise Exception("Unsupported R-format instruction/funct field error")

    def populate_immediate(self):
        if self.format == "I":
            self.immediate = create_sized_binary_num(self._arg3, 16)

    def populate_address(self):
        if self.format == "J":
            self.address = create_sized_binary_num(self._arg1, 26)

    def binary_version(self):
        return self.full_binary_rep

    def asm_version(self):

        return self.name + " " + str(self._arg1) + " "+ str(self._arg2) + " " + str(self._arg3)
