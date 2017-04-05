import unittest
from PipelineInterface import PipelineInterface
from Instruction import Instruction, decode_signed_binary_number, create_sized_binary_num


class PipelineInterfaceTest(unittest.TestCase):
    var_exit = '500'
    var_else = '550'
    var_end = '600'

    starting_address = 0

    Instruction_list = [Instruction('Add', "$t1", "$t2", "t3"), Instruction('addi', '$t8', '$zero', '1'),
                        Instruction('addi', '$t4', '$zero', '257'), Instruction('beq', '$a1', '$zero', var_exit),
                        Instruction('sub', '$a1', '$a1', '$t8'), Instruction('lw', '$t0', '$a0', '0'),
                        Instruction('slt', '$t1', '$t0', '$t4'), Instruction('bne', '$t0', '$zero', var_else),
                        Instruction('div', '$v0', '$v0', '$t7'), Instruction('or', '$s1', '$s1', '$v0'),
                        Instruction('sw', '$t6', '$a0', '0'), Instruction('j', var_end),
                        Instruction('mult', '$s2', '$s1', '$t3'), Instruction('xor', '$s3', '$s3', '$s2')]

    register_file = [create_sized_binary_num(65535, 32) for i in range(0, 32)]  # empty register files

    data_memory_addresses = [create_sized_binary_num(i, 32) for i in range(0, 512)]
    data_memory = {}
    for i in data_memory_addresses:
        data_memory[i] = create_sized_binary_num(0, 32)

    def test_execute_add_instruction(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()

        this_register_file[10] = create_sized_binary_num(12, 32)  # put something in register $t2
        this_register_file[11] = create_sized_binary_num(18, 32)  # put something in register $t3

        interface = PipelineInterface(PipelineInterfaceTest.Instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(30, 32), interface.retrieve_register_list()[9])


if __name__ == '__main__':
    unittest.main()
