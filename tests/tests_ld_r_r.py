import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_ld_r_r(unittest.TestCase):

    def test_ld_B_A_works_correctly(self):
        cpu = CPU(ROM(b'\x47'))
        cpu.A = 0x5D
        cpu.B = 0x11
        cpu.readOp()
        self.assertEqual(0x5d, cpu.B)
        self.assertEqual(0x5d, cpu.A)

    def test_ld_B_A_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\x47'))
        cpu.A = 0x5D
        cpu.B = 0x11
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ld_B_A_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x47'))
        cpu.A = 0x5D
        cpu.B = 0x11
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
