import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_and_a(unittest.TestCase):
    def test_and_a_performs_and_operation(self):
        cpu = CPU(ROM(b'\xa7'))
        cpu.A = 0x12
        cpu.readOp()
        self.assertEqual(0x12, cpu.A)

    def test_and_a_sets_HFlag(self):
        cpu = CPU(ROM(b'\xa7'))
        cpu.A = 0x12
        cpu.HFlag = False
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_and_a_resets_n_and_c_flag(self):
        cpu = CPU(ROM(b'\xa7'))
        cpu.CFlag = True
        cpu.NFlag = True
        cpu.readOp()
        self.assertFalse(cpu.CFlag)
        self.assertFalse(cpu.NFlag)

    def test_and_a_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\xa7'))
        cpu.A = 0x12
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_and_a_takes_4_t_states(self):
        cpu = CPU(ROM(b'\xa7'))
        cpu.A = 0x12
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
