import unittest

from Stages import Decode, Execute
from Instruction import Instruction


class MyTestCase(unittest.TestCase):
    register_file = [None for i in range(0, 32)]  # empty register files

    def test_create_decode(self):
        decode = Decode(self.register_file, Execute())
        self.assertEqual(None, decode.read_reg_1)
        self.assertEqual(None, decode.read_reg_2)
        self.assertEqual(None, decode.write_register)

    def test_receive_instruction(self):
        decode = Decode(self.register_file, Execute())
        decode.receive_instruction(Instruction('Add', "$t1", "$t2", "t3"))
        self.assertEqual("01001", decode.write_register)
        self.assertEqual("01010", decode.read_reg_1)
        self.assertEqual("01011", decode.read_reg_2)

    def test_write_to_write_reg(self):
        decode = Decode(self.register_file, Execute())
        decode.receive_instruction(Instruction('Add', "$t1", "$t2", "t3"))
        decode.write_to_register("Test data.")
        self.assertEqual("Test data.", decode.register_file[9])

    def test_extend_immediate(self):
        decode = Decode(self.register_file, Execute())
        decode.receive_instruction(Instruction('addi', '$t8', '$zero', '1'))
        self.assertEqual("00000000000000000000000000000001", decode.sign_extended_immediate)

    def test_extend_immediate_neg(self):
        decode = Decode(self.register_file, Execute())
        decode.receive_instruction(Instruction('addi', '$t8', '$zero', '-10'))
        self.assertEqual("11111111111111111111111111110110", decode.sign_extended_immediate)


if __name__ == '__main__':
    unittest.main()
