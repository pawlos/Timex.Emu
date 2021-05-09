import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_rlca(unittest.TestCase):

    def test_rlca_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\x07'))
        cpu.A = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlca_rotates_correctly(self):
        cpu = CPU(ROM(b'\x07'))
        cpu.A = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.A)

    def test_rlca_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\x07'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_rlca_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x07'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
