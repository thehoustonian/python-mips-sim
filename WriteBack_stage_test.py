import unittest

from Stages import *
from Instruction import create_sized_binary_num, decode_signed_binary_number


class WriteBackStageTest(unittest.TestCase):
    def test_send_jump_address(self):
        wb = WriteBack()
        jump = True
        MemtoReg = False
        jump_address = create_sized_binary_num(23, 32)
        pc_address = create_sized_binary_num(48, 32)
        mem_data = create_sized_binary_num(64, 32)
        alu_data = create_sized_binary_num(128, 32)

        wb.receive_control_information(jump, MemtoReg, True)
        with self.assertRaises(Exception) as cm:
            wb.receive_data(jump_address, pc_address, mem_data, alu_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(jump_address, wb.new_pc_address)

    def test_send_pc_address(self):
        wb = WriteBack()
        jump = False
        MemtoReg = False
        jump_address = create_sized_binary_num(23, 32)
        pc_address = create_sized_binary_num(48, 32)
        mem_data = create_sized_binary_num(64, 32)
        alu_data = create_sized_binary_num(128, 32)

        wb.receive_control_information(jump, MemtoReg, False)
        with self.assertRaises(Exception) as cm:
            wb.receive_data(jump_address, pc_address, mem_data, alu_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(pc_address, wb.new_pc_address)

    def test_send_read_data(self):
        wb = WriteBack()
        jump = False
        MemtoReg = True
        jump_address = create_sized_binary_num(23, 32)
        pc_address = create_sized_binary_num(48, 32)
        mem_data = create_sized_binary_num(64, 32)
        alu_data = create_sized_binary_num(128, 32)

        wb.receive_control_information(jump, MemtoReg, False)
        with self.assertRaises(Exception) as cm:
            wb.receive_data(jump_address, pc_address, mem_data, alu_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(pc_address, wb.new_pc_address)
        self.assertEqual(mem_data, wb.reg_data)

    def test_send_alu_data(self):
        wb = WriteBack()
        jump = False
        MemtoReg = False
        jump_address = create_sized_binary_num(23, 32)
        pc_address = create_sized_binary_num(48, 32)
        mem_data = create_sized_binary_num(64, 32)
        alu_data = create_sized_binary_num(128, 32)

        wb.receive_control_information(jump, MemtoReg, False)
        with self.assertRaises(Exception) as cm:
            wb.receive_data(jump_address, pc_address, mem_data, alu_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(pc_address, wb.new_pc_address)
        self.assertEqual(alu_data, wb.reg_data)

if __name__ == '__main__':
    unittest.main()
