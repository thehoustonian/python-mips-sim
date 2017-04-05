import unittest
from PipelineInterface import PipelineInterface
from Instruction import Instruction, decode_signed_binary_number, create_sized_binary_num, decode_asm_register


class PipelineInterfaceTest(unittest.TestCase):
    var_exit = '5'
    var_else = '7'
    var_end = '10'

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
        starting_address = 0

        this_register_file[10] = create_sized_binary_num(12, 32)  # put something in register $t2
        this_register_file[11] = create_sized_binary_num(18, 32)  # put something in register $t3

        interface = PipelineInterface(PipelineInterfaceTest.Instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(30, 32), interface.retrieve_register_list()[9])

    def test_execute_addi_instruction(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[1:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(1, 32), interface.retrieve_register_list()[decode_asm_register('t8')])

    def test_execute_addi_instruction_2(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[2:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(257, 32), interface.retrieve_register_list()[decode_asm_register('t4')])

    def test_execute_beq_do_branch(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_register_file[decode_asm_register('a1')] = create_sized_binary_num(0, 32)
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[3:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()

        expected_address = int(
            PipelineInterfaceTest.var_exit) * 4 + 4  # branch addresses are multiplied by 4 and relative to pc + 4

        self.assertEqual(expected_address, interface.retrieve_current_pc_address())

    def test_execute_beq_not_taken(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_register_file[decode_asm_register('a1')] = create_sized_binary_num(20, 32)
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[3:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()

        expected_address = int(
            PipelineInterfaceTest.starting_address)+ 4  # branch addresses are multiplied by 4 and relative to pc + 4

        self.assertEqual(expected_address, interface.retrieve_current_pc_address())

    def test_execute_sub(self):
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[4:]

        this_register_file[decode_asm_register('a1')] = create_sized_binary_num(24, 32)  # put something in register $t2
        this_register_file[decode_asm_register('t8')] = create_sized_binary_num(18, 32)  # put something in register $t3

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(24-18, 32), interface.retrieve_register_list()[decode_asm_register('a1')])

    def test_execute_lw(self):
        # lw $t0, $a0, 0 (0 is the offset amount)
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[5:]
        this_memory_file = PipelineInterfaceTest.data_memory.copy()
        this_memory_file[create_sized_binary_num(4, 32)] = create_sized_binary_num(1995, 32)

        this_register_file[decode_asm_register('a0')] = create_sized_binary_num(4, 32)

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      this_memory_file)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(1995, 32),
                         interface.retrieve_register_list()[decode_asm_register('t0')])

    def test_execute_slt_is_set(self):
        # slt $t1, $t0, $t4
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[6:]
        this_memory_file = PipelineInterfaceTest.data_memory.copy()

        this_register_file[decode_asm_register('t0')] = create_sized_binary_num(4, 32)
        this_register_file[decode_asm_register('t4')] =  create_sized_binary_num(22, 32)

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      this_memory_file)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(1, 32),
                         interface.retrieve_register_list()[decode_asm_register('t1')])

    def test_execute_slt_not_set(self):
        # slt $t1, $t0, $t4
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[6:]
        this_memory_file = PipelineInterfaceTest.data_memory.copy()

        this_register_file[decode_asm_register('t0')] = create_sized_binary_num(22, 32)
        this_register_file[decode_asm_register('t4')] = create_sized_binary_num(4, 32)

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      this_memory_file)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(0, 32),
                         interface.retrieve_register_list()[decode_asm_register('t1')])

    def test_execute_bne_no_branch(self):
        # bne $t0, $zero, var_else where var_else is an address
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_register_file[decode_asm_register('t0')] = create_sized_binary_num(0, 32)
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[7:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()

        expected_address = int(
            PipelineInterfaceTest.starting_address) + 4  # branch addresses are multiplied by 4 and relative to pc + 4

        self.assertEqual(expected_address, interface.retrieve_current_pc_address())

    def test_execute_bne_do_branch(self):
        # bne $t0, $zero, var_else where var_else is an address
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_register_file[decode_asm_register('t0')] = create_sized_binary_num(1984, 32)
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[7:]

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()

        expected_address = int(
            PipelineInterfaceTest.var_else) * 4 + 4  # branch addresses are multiplied by 4 and relative to pc + 4

        self.assertEqual(expected_address, interface.retrieve_current_pc_address())

    def test_execute_div(self):
        # div $v0, $v0, $t7
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[8:]

        this_register_file[decode_asm_register('v0')] = create_sized_binary_num(24, 32)  # put something in register $t2
        this_register_file[decode_asm_register('t7')] = create_sized_binary_num(18, 32)  # put something in register $t3

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(24 / 18, 32),
                         interface.retrieve_register_list()[decode_asm_register('v0')])

    def test_execute_or(self):
        # or $s1, $s1, $v0
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[9:]

        this_register_file[decode_asm_register('s1')] = create_sized_binary_num(2000, 32)  # put something in register $t2
        this_register_file[decode_asm_register('v0')] = create_sized_binary_num(2017, 32)  # put something in register $t3

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(2000 | 2017, 32),
                         interface.retrieve_register_list()[decode_asm_register('s1')])

    def test_execute_sw(self):
        # sw $t6, $a0, 0 (0 is the offset amount)
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[10:]
        this_memory_file = PipelineInterfaceTest.data_memory.copy()

        this_register_file[decode_asm_register('a0')] = create_sized_binary_num(4, 32)
        this_register_file[decode_asm_register('t6')] = create_sized_binary_num(1995, 32)

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      this_memory_file)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(1995, 32),
                         interface.retrieve_data_memory()[create_sized_binary_num(4,32)])

    def test_execute_j(self):
        # j  var_end, where var_end is the address to jump to
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[11:]
        this_memory_file = PipelineInterfaceTest.data_memory.copy()

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      this_memory_file)
        expected_address = int(PipelineInterfaceTest.var_end)*4
        interface.trigger_clock_cycle()
        self.assertEqual(expected_address,
                         interface.retrieve_current_pc_address())

    def test_execute_mult(self):
        # mult $s2, $s1, $t3
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[12:]

        this_register_file[decode_asm_register('s1')] = create_sized_binary_num(54, 32)  # put something in register $t2
        this_register_file[decode_asm_register('t3')] = create_sized_binary_num(2000, 32)  # put something in register $t3

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(54 * 2000, 32),
                         interface.retrieve_register_list()[decode_asm_register('s2')])

    def test_execute_xor(self):
        # xor $s3, $s3, $s2
        this_register_file = PipelineInterfaceTest.register_file.copy()
        this_instruction_list = PipelineInterfaceTest.Instruction_list.copy()[13:]

        this_register_file[decode_asm_register('s3')] = create_sized_binary_num(24, 32)  # put something in register $t2
        this_register_file[decode_asm_register('s2')] = create_sized_binary_num(18, 32)  # put something in register $t3

        interface = PipelineInterface(this_instruction_list,
                                      PipelineInterfaceTest.starting_address,
                                      this_register_file,
                                      PipelineInterfaceTest.data_memory)
        interface.trigger_clock_cycle()
        self.assertEqual(create_sized_binary_num(24 ^ 18, 32),
                         interface.retrieve_register_list()[decode_asm_register('s3')])

if __name__ == '__main__':
    unittest.main()
