import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_rrca(unittest.TestCase):

    def test_rrca_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\x0f'))
        cpu.A = 0b00010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rrca_rotates_correctly(self):
        cpu = CPU(ROM(b'\x0f'))
        cpu.A = 0b00010001
        cpu.readOp()
        self.assertEqual(0x88, cpu.A)

    def test_rrca_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\x0f'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_rrca_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x0f'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
