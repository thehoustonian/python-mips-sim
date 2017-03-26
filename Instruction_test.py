import unittest
from Instruction import Instruction

# TODO: Add tests for more instructions before doing anything with pipeline stages

class TestKnownInstructionConversion(unittest.TestCase):
    def test_add_instruction(self):
        self.assertEqual('00000001010010110100100000100000', Instruction('Add', "$t1", "$t2", "t3").binary_version())


if __name__ == '__main__':
    unittest.main()
