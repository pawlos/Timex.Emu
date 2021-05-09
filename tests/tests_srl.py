import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_srl(unittest.TestCase):

    def test_srl_h_does_shift_h_correctly(self):
        cpu = CPU(ROM(b'\xcb\x3c'))
        cpu.H = 0b11110000
        cpu.readOp()
        self.assertEqual(0b01111000, cpu.H)

    def test_srl_h_does_set_Cflag_correctly(self):
        cpu = CPU(ROM(b'\xcb\x3c'))
        cpu.H = 0b11110001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_srl_h_does_take_2_m_cycles(self):
        cpu = CPU(ROM(b'\xcb\x3c'))
        cpu.H = 0b11110001
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_srl_h_does_take_8_t_states(self):
        cpu = CPU(ROM(b'\xcb\x3c'))
        cpu.H = 0b11110001
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)
