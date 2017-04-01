import unittest
from Instruction import Instruction
from Stages import Fetch
"""
Unit tests for the Fetch class that represents the Fetch stage of a MIPS pipeline
Author: Trey Franklin
Created: 3/28/2017
Modified: 3/28/2017
"""


class MyTestCase(unittest.TestCase):
    var_exit = '256'
    var_else = '256'
    var_end = '320'
    Instruction_list = [Instruction('Add', "$t1", "$t2", "t3"), Instruction('addi', '$t8', '$zero', '1'),
                        Instruction('addi', '$t4', '$zero', '257'), Instruction('beq', '$a1', '$zero', var_exit),
                        Instruction('sub', '$a1', '$a1', '$t8'), Instruction('lw', '$t0', '$a0', '0'),
                        Instruction('slt', '$t1', '$t0', '$t4'), Instruction('bne', '$t0', '$zero', var_else),
                        Instruction('div', '$v0', '$v0', '$t7'), Instruction('or', '$s1', '$s1', '$v0'),
                        Instruction('sw', '$t6', '$a0', '0'), Instruction('j', var_end),
                        Instruction('mult', '$s2', '$s1', '$t3'), Instruction('xor', '$s3', '$s3', '$s2')]

    def test_create_fetch_with_values(self):

        self.assertEqual(0, Fetch(MyTestCase.Instruction_list, '0').program_counter)

    def test_increment_program_counter_bad_value(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        with self.assertRaises(Exception) as cm:
            fetch_object.update_program_counter(2)
        self.assertTrue("Invalid Program Counter Value!" in str(cm.exception))

    def test_increment_program_counter_good_value(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        fetch_object.update_program_counter(4)
        self.assertEqual(4, fetch_object.program_counter)

    def test_fetch_instruction_from_start_address(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        self.assertEqual(MyTestCase.Instruction_list[0].binary_version(), fetch_object.fetch_instruction().binary_version())

    def test_increment_pc_and_fetch_instruction(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        fetch_object.update_program_counter(4)
        self.assertEqual(MyTestCase.Instruction_list[1].binary_version(), fetch_object.fetch_instruction().binary_version())

    def test_fetch_instruction_bad_address_breaks(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        fetch_object.update_program_counter(60)
        with self.assertRaises(Exception) as cm:
            fetch_object.fetch_instruction()
        self.assertTrue("Invalid Instruction Address!" in str(cm.exception))

    def test_fetch_instruction_increment_program_counter(self):
        fetch_object = Fetch(MyTestCase.Instruction_list, '0')
        self.assertEqual(0, fetch_object.program_counter)
        fetch_object.increment_program_counter()
        self.assertEqual(4, fetch_object.program_counter)

if __name__ == '__main__':
    unittest.main()
