"""
This is the python implementation of the provided test program to see the expected functionality
Trey Franklin
"""
from Instruction import create_sized_binary_num


def python_test_program():
    """
    Implements the test program that was provided in Python to view expected results.
    :return: array of values calculated.
    """
    v0 = 0x0040
    v1 = 0x1010
    s2 = 0x000F
    s3 = 0x00F0
    t0 = 0x0000
    a0 = 0x0010
    a1 = 0x0005

    data_mem = {16: 0x0101, 20: 0x0110, 24: 0x0011, 28: 0x00F0, 32: 0x00FF}

    while a1 > 0:
        a1 = a1 - 1
        t0 = data_mem[a0]
        if t0 > 0x0100:
            v0 = int(v0 / 8)
            v1 = v1 | v0
            data_mem[a0] = create_sized_binary_num(0x7F00, 32)
        else:
            s2 = s2 * 4
            s3 = s3 ^ s2
            data_mem[a0] = create_sized_binary_num(0x00FF, 32)
        a0 = a0 + 4
    """
    print("data mem: ", data_mem)
    print("v0: ", v0)
    print("v1: ", v1)
    print("s2: ", s2)
    print("s3: ", s3)
    print("t0: ", t0)
    print("a0: ", a0)
    print("a1: ", a1)
    """

    return [data_mem, v0, v1, s2, s3, t0, a0, a1]