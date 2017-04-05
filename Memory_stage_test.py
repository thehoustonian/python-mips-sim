import unittest

from Stages import Memory, WriteBack
from Instruction import create_sized_binary_num, decode_signed_binary_number


class MemoryStageTest(unittest.TestCase):
    data_memory_addresses = [create_sized_binary_num(i, 32) for i in range(0, 512)]
    data_memory = {}
    for i in data_memory_addresses:
        data_memory[i] = create_sized_binary_num(0, 32)

    def test_create_memory(self):
        mem = Memory(MemoryStageTest.data_memory, WriteBack())
        self.assertEqual(MemoryStageTest.data_memory, mem.memory)

    def test_read_memory(self):
        this_data_mem = MemoryStageTest.data_memory.copy()
        this_data_mem[create_sized_binary_num(16, 32)] = create_sized_binary_num(22, 32)

        mem = Memory(this_data_mem, WriteBack())

        branch = False
        alu_branch = False
        MemWrite = False
        MemRead = True
        MemtoReg = True
        jump = False

        pc = create_sized_binary_num(8, 32)
        ja = create_sized_binary_num(0, 32)
        alu_output = create_sized_binary_num(16, 32)
        branch_addr = create_sized_binary_num(4, 32)
        write_data = None

        mem.receive_control_info(branch, alu_branch, MemWrite, MemRead, MemtoReg, jump)
        with self.assertRaises(Exception) as cm:
            mem.receive_data(pc, ja, alu_output, branch_addr, write_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(create_sized_binary_num(22, 32), mem.read_data)

    def test_write_memory(self):
        this_data_mem = MemoryStageTest.data_memory.copy()

        mem = Memory(this_data_mem, WriteBack())

        branch = False
        alu_branch = False
        MemWrite = True
        MemRead = False
        MemtoReg = False
        jump = False

        pc = create_sized_binary_num(8, 32)
        ja = create_sized_binary_num(0, 32)
        alu_output = create_sized_binary_num(16, 32)
        branch_addr = create_sized_binary_num(4, 32)
        write_data = create_sized_binary_num(31, 32)

        mem.receive_control_info(branch, alu_branch, MemWrite, MemRead, MemtoReg, jump)
        with self.assertRaises(Exception) as cm:
            mem.receive_data(pc, ja, alu_output, branch_addr, write_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(create_sized_binary_num(31, 32), mem.memory[alu_output])

    def test_branch_decision_expect_false(self):
        this_data_mem = MemoryStageTest.data_memory.copy()

        mem = Memory(this_data_mem, WriteBack())

        branch = True
        alu_branch = False
        MemWrite = False
        MemRead = False
        MemtoReg = False
        jump = False

        pc = create_sized_binary_num(8, 32)
        ja = create_sized_binary_num(0, 32)
        alu_output = create_sized_binary_num(16, 32)
        branch_addr = create_sized_binary_num(4, 32)
        write_data = None

        mem.receive_control_info(branch, alu_branch, MemWrite, MemRead, MemtoReg, jump)
        with self.assertRaises(Exception) as cm:
            mem.receive_data(pc, ja, alu_output, branch_addr, write_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(pc, mem.pc_address)

    def test_branch_decision_expect_true(self):
        this_data_mem = MemoryStageTest.data_memory.copy()

        mem = Memory(this_data_mem, WriteBack())

        branch = True
        alu_branch = True
        MemWrite = False
        MemRead = False
        MemtoReg = False
        jump = False

        pc = create_sized_binary_num(8, 32)
        ja = create_sized_binary_num(0, 32)
        alu_output = create_sized_binary_num(16, 32)
        branch_addr = create_sized_binary_num(4, 32)
        write_data = None

        mem.receive_control_info(branch, alu_branch, MemWrite, MemRead, MemtoReg, jump)
        with self.assertRaises(Exception) as cm:
            mem.receive_data(pc, ja, alu_output, branch_addr, write_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(branch_addr, mem.pc_address)

    def test_jump_address(self):
        this_data_mem = MemoryStageTest.data_memory.copy()

        mem = Memory(this_data_mem, WriteBack())

        branch = True
        alu_branch = False
        MemWrite = False
        MemRead = False
        MemtoReg = False
        jump = False

        pc = create_sized_binary_num(8, 32)
        ja = create_sized_binary_num(0, 32)
        alu_output = create_sized_binary_num(16, 32)
        branch_addr = create_sized_binary_num(4, 32)
        write_data = None

        mem.receive_control_info(branch, alu_branch, MemWrite, MemRead, MemtoReg, jump)
        with self.assertRaises(Exception) as cm:
            mem.receive_data(pc, ja, alu_output, branch_addr, write_data)
        self.assertTrue("(WriteBack): Error! No stages to write data back to." in str(cm.exception))
        self.assertEqual(ja, mem.jump_address)

if __name__ == '__main__':
    unittest.main()
