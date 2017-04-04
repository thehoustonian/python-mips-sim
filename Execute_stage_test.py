import unittest
from Stages import Execute
from Instruction import create_sized_binary_num, decode_signed_binary_number


class MyTestCase(unittest.TestCase):
    data1 = '00000000000000001111000011110000'
    data2 = '11111111111111110000111100001111'
    immediate = '00000000000000000111111111111111'
    neg_immediate = '11111111111111111000000000000000'
    pc_value = 8

    def test_create_execute_object_default_values(self):
        execute = Execute()
        self.assertEqual(None, execute.ALUOp)
        self.assertEqual(None, execute.ALUSrc)
        self.assertEqual(None, execute.function_code)
        self.assertEqual(None, execute.opcode)
        self.assertEqual(None, execute.immediate)
        self.assertEqual(None, execute.read_data1)
        self.assertEqual(None, execute.read_data2)
        self.assertEqual(None, execute.operation)
        self.assertEqual(False, execute.branch_equal)
        self.assertEqual(False, execute.branch_not_equal)
        self.assertEqual(None, execute.alu_input_1)
        self.assertEqual(None, execute.alu_input_2)
        self.assertEqual(None, execute.alu_output)
        self.assertEqual(None, execute.alu_branch)

    def test_receive_values_and_update_lw(self):
        execute = Execute()

        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) +
                                                  decode_signed_binary_number(MyTestCase.immediate, 32), 32)[:32]

        ALUOp = 0b00
        function_field = None
        opcode = None
        ALUSrc = True
        MemWrite = False
        MemtoReg = True
        MemRead = True
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_add(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) +
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = '100000'
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_addi(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) +
                                                  decode_signed_binary_number(MyTestCase.immediate, 32), 32)[:32]

        ALUOp = 0b11
        function_field = '100000'
        opcode = create_sized_binary_num(8, 6)
        ALUSrc = True
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_addi_neg(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) +
                                                  decode_signed_binary_number(MyTestCase.neg_immediate, 32), 32)[:32]

        ALUOp = 0b11
        function_field = '100000'
        opcode = create_sized_binary_num(8, 6)
        ALUSrc = True
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.neg_immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_andi(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) &
                                                  decode_signed_binary_number(MyTestCase.immediate, 32), 32)[:32]

        ALUOp = 0b11
        function_field = '100000'
        opcode = create_sized_binary_num(12, 6)
        ALUSrc = True
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_sw(self):
        execute = Execute()

        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) +
                                                  decode_signed_binary_number(MyTestCase.immediate, 32), 32)[:32]

        ALUOp = 0b00
        function_field = None
        opcode = None
        ALUSrc = True
        MemWrite = True
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_and(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) &
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(36, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_div(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) /
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(26, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_receive_values_and_update_or(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) |
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(37, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_mul(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) *
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(24, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_slt(self):
        execute = Execute()
        expected_result = create_sized_binary_num(0, 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(42, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_slt_set(self):
        execute = Execute()
        expected_result = create_sized_binary_num(1, 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(42, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data2, MyTestCase.data1, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_sub(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) -
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(34, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_xor(self):
        execute = Execute()
        expected_result = create_sized_binary_num(decode_signed_binary_number(MyTestCase.data1, 32) ^
                                                  decode_signed_binary_number(MyTestCase.data2, 32), 32)[:32]

        ALUOp = 0b10
        function_field = create_sized_binary_num(38, 6)
        opcode = None
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = False
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(expected_result, execute.alu_output)

    def test_branch_if_equal_true(self):
        execute = Execute()
        alu_branch_output = True
        alu_output = create_sized_binary_num(0, 32)
        branch_address = create_sized_binary_num(MyTestCase.pc_value +
                                                 (decode_signed_binary_number(MyTestCase.immediate, 32) << 2), 32)[:32]

        ALUOp = 0b01
        function_field = create_sized_binary_num(4, 6)
        opcode = '000100'
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = True
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data1, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(alu_branch_output, execute.alu_branch)
        self.assertEqual(alu_output, execute.alu_output)
        self.assertEqual(branch_address, execute.branch_address)

    def test_branch_if_equal_false(self):
        execute = Execute()
        alu_branch_output = False
        branch_address = create_sized_binary_num(MyTestCase.pc_value +
                                                 (decode_signed_binary_number(MyTestCase.immediate, 32) << 2), 32)[:32]

        ALUOp = 0b01
        function_field = create_sized_binary_num(4, 6)
        opcode = '000100'
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = True
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(alu_branch_output, execute.alu_branch)
        self.assertEqual(branch_address, execute.branch_address)

    def test_branch_if_not_equal_false(self):
        execute = Execute()
        alu_branch_output = False
        alu_output = create_sized_binary_num(0, 32)
        branch_address = create_sized_binary_num(MyTestCase.pc_value +
                                                 (decode_signed_binary_number(MyTestCase.immediate, 32) << 2), 32)[:32]

        ALUOp = 0b01
        function_field = create_sized_binary_num(4, 6)
        opcode = '000101'
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = True
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data1, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(alu_branch_output, execute.alu_branch)
        self.assertEqual(alu_output, execute.alu_output)
        self.assertEqual(branch_address, execute.branch_address)

    def test_branch_if_not_equal_true(self):
        execute = Execute()
        alu_branch_output = True
        branch_address = create_sized_binary_num(MyTestCase.pc_value +
                                                 (decode_signed_binary_number(MyTestCase.immediate, 32) << 2), 32)[:32]

        ALUOp = 0b01
        function_field = create_sized_binary_num(4, 6)
        opcode = '000101'
        ALUSrc = False
        MemWrite = False
        MemtoReg = False
        MemRead = False
        Branch = True
        jump = False
        jump_address = None

        execute.receive_data(MyTestCase.data1, MyTestCase.data2, MyTestCase.immediate, MyTestCase.pc_value, jump_address)
        execute.receive_control_information(ALUOp, function_field, opcode, ALUSrc, MemWrite, MemtoReg, MemRead,
                                            Branch, jump)
        self.assertEqual(alu_branch_output, execute.alu_branch)
        self.assertEqual(branch_address, execute.branch_address)

if __name__ == '__main__':
    unittest.main()
