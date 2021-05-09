import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_rra(unittest.TestCase):

    def test_rra_does_modify_value_correctly(self):
        cpu = CPU(ROM(b'\x1f'))
        cpu.A = 0b11100001
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0b01110000, cpu.A)
        self.assertTrue(cpu.CFlag)

    def test_rra_does_take_1_m_cycles(self):
        cpu = CPU(ROM(b'\x1f'))
        cpu.A = 0b11100001
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_rra_does_take_4_t_states(self):
        cpu = CPU(ROM(b'\x1f'))
        cpu.A = 0b11100001
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
