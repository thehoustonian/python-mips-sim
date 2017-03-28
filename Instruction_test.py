import unittest
from Instruction import Instruction


class TestKnownInstructionConversion(unittest.TestCase):
    def test_add_instruction(self):
        self.assertEqual('00000001010010110100100000100000', Instruction('Add', "$t1", "$t2", "t3").binary_version())

    def test_addi_instruction(self):  # addi $t8, $zero, 1
        self.assertEqual('00100000000110000000000000000001', Instruction('addi', '$t8', '$zero', '1').binary_version())

    def test_addi_hex_instruction(self):
        self.assertEqual('00100000000011000000000100000001', Instruction('addi', '$t4', '$zero', '257').binary_version())

    def test_beq_instruction(self):
        var_exit = '256'  # address to branch to
        self.assertEqual('00010000101000000000000100000000', Instruction('beq', '$a1', '$zero', var_exit).binary_version())

    def test_sub_instruction(self):
        self.assertEqual('00000000101110000010100000100010', Instruction('sub', '$a1', '$a1', '$t8').binary_version())

    def test_lw_instruction(self):  # lw $t0, $a0, 0
        self.assertEqual('10001100100010000000000000000000', Instruction('lw', '$t0', '$a0', '0').binary_version())

    def test_slt_instruction(self):
        self.assertEqual('00000001000011000100100000101010', Instruction('slt', '$t1', '$t0', '$t4').binary_version())

    def test_bne_instruction(self):  # this might not actually be testing correctly, tbh
        var_else = '256'
        self.assertEqual('00010101000000000000000100000000', Instruction('bne', '$t0', '$zero', var_else).binary_version())

    def test_div_instruction(self):  # This is a pseudo-instruction so my binary doesn't match mips
        self.assertEqual('00000000010011110001000000011010', Instruction('div', '$v0', '$v0', '$t7').binary_version())

    def test_or_instruction(self):
        self.assertEqual('00000010001000101000100000100101', Instruction('or', '$s1', '$s1', '$v0').binary_version())

    def test_sw_instruction(self):
        self.assertEqual('10101100100011100000000000000000', Instruction('sw', '$t6', '$a0', '0').binary_version())

    def test_j_instruction(self):
        var_end = '320'
        self.assertEqual('00001000000000000000000101000000', Instruction('j', var_end).binary_version())

    def test_mult_instruction(self):
        self.assertEqual('00000010001010111001000000011000', Instruction('mult', '$s2', '$s1', '$t3').binary_version())

    def test_xor_instruction(self):
        self.assertEqual('00000010011100101001100000100110', Instruction('xor', '$s3', '$s3', '$s2').binary_version())

if __name__ == '__main__':
    unittest.main()
