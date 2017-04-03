import unittest
from control import Control


class MyTestCase(unittest.TestCase):
    def test_create_control(self):
        control = Control()
        self.assertEqual(None, control.RegDst)
        self.assertEqual(None, control.ALUSrc)
        self.assertEqual(None, control.MemtoReg)
        self.assertEqual(None, control.RegWrite)
        self.assertEqual(None, control.MemRead)
        self.assertEqual(None, control.MemWrite)
        self.assertEqual(None, control.Branch)
        self.assertEqual(None, control.ALUOp)
        self.assertEqual(None, control.jump)

    def test_control_r_format(self):
        control = Control()
        control.update(0)
        self.assertEqual(True, control.RegDst)
        self.assertEqual(False, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(True, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b10, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_lw(self):
        control = Control()
        control.update(35)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(True, control.ALUSrc)
        self.assertEqual(True, control.MemtoReg)
        self.assertEqual(True, control.RegWrite)
        self.assertEqual(True, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b00, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_sw(self):
        control = Control()
        control.update(43)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(True, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(False, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(True, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b00, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_beq(self):
        control = Control()
        control.update(4)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(False, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(False, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(True, control.Branch)
        self.assertEqual(0b01, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_bne(self):
        control = Control()
        control.update(5)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(False, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(False, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(True, control.Branch)
        self.assertEqual(0b01, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_addi(self):
        control = Control()
        control.update(8)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(True, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(True, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b11, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_andi(self):
        control = Control()
        control.update(12)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(True, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(True, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b11, control.ALUOp)
        self.assertEqual(False, control.jump)

    def test_control_jump(self):
        control = Control()
        control.update(2)
        self.assertEqual(False, control.RegDst)
        self.assertEqual(False, control.ALUSrc)
        self.assertEqual(False, control.MemtoReg)
        self.assertEqual(False, control.RegWrite)
        self.assertEqual(False, control.MemRead)
        self.assertEqual(False, control.MemWrite)
        self.assertEqual(False, control.Branch)
        self.assertEqual(0b01, control.ALUOp)
        self.assertEqual(True, control.jump)


if __name__ == '__main__':
    unittest.main()
