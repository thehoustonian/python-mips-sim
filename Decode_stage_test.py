import unittest

from Stages import Decode, Execute, WriteBack
from Instruction import Instruction, create_sized_binary_num


class DecodeStageTest(unittest.TestCase):
    register_file = [create_sized_binary_num(65535, 32) for i in range(0, 32)]  # empty register files

    def test_create_decode(self):
        decode = Decode(self.register_file)
        self.assertEqual(None, decode.read_reg_1)
        self.assertEqual(None, decode.read_reg_2)
        self.assertEqual(None, decode.write_register)

    def test_receive_instruction(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('Add', "$t1", "$t2", "t3"), 8)
        self.assertEqual("01001", decode.write_register)
        self.assertEqual("01010", decode.read_reg_1)
        self.assertEqual("01011", decode.read_reg_2)

    def test_write_to_write_reg(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('Add', "$t1", "$t2", "t3"), 8)
        decode.write_to_register("Test data.")
        self.assertEqual("Test data.", decode.register_file[9])

    def test_correct_values_in_register_file(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('add', '$t1', '$t2', '$t3'), 8)
        for value in decode.register_file[1:]:
            self.assertEqual('00000000000000001111111111111111', value)

    def test_extend_immediate(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('addi', '$t8', '$zero', '1'), 8)
        self.assertEqual("00000000000000000000000000000001", decode.sign_extended_immediate)

    def test_extend_immediate_neg(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('addi', '$t8', '$zero', '-10'), 8)
        self.assertEqual("11111111111111111111111111110110", decode.sign_extended_immediate)

    def test_calculate_jump_address(self):
        decode = Decode(self.register_file)
        decode.receive_instruction(Instruction('j', '320'), 8)
        self.assertEqual("00000000000000000000010100000000", decode.jump_address)


if __name__ == '__main__':
    unittest.main()
