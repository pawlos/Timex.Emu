import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_jrc(unittest.TestCase):

    def test_jr_c_jumps_forward_when_carry_set(self):
        # JR C, +5 at address 0x0000
        # opcode 0x38, displacement 0x05
        # After reading opcode+displacement, PC = 0x0002
        # Jump target = 0x0002 + 5 = 0x0007
        ram = RAM()
        cpu = CPU(ROM(b'\x38\x05'), ram)
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(0x0007, cpu.PC)

    def test_jr_c_jumps_backward_when_carry_set(self):
        # JR C, -4 at address 0x0010
        # opcode 0x38, displacement 0xFC (-4 in two's complement)
        # After reading opcode+displacement, PC = 0x0012
        # Jump target = 0x0012 + (-4) = 0x000E
        ram = RAM()
        cpu = CPU(ROM(b'\x00' * 0x10 + b'\x38\xfc'), ram)
        cpu.PC = 0x0010
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(0x000E, cpu.PC)

    def test_jr_c_no_jump_when_carry_not_set(self):
        # JR C, +5 — carry not set, should not jump
        # PC should advance past the 2-byte instruction to 0x0002
        ram = RAM()
        cpu = CPU(ROM(b'\x38\x05'), ram)
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x0002, cpu.PC)
