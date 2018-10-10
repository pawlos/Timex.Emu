import unittest
from cpu import CPU
from rom import ROM


class tests_ldar(unittest.TestCase):

    def test_ldar_copies_correct_value_from_R_to_A(self):
        cpu = CPU(ROM('\xed\x5f'))
        cpu.R = 0x11
        cpu.readOp()
        self.assertEqual(0x11, cpu.A)

    def test_ldar_takes_2_m_cycles(self):
        cpu = CPU(ROM('\xed\x5f'))
        cpu.R = 0x11
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ldar_takes_9_t_states(self):
        cpu = CPU(ROM('\xed\x5f'))
        cpu.R = 0x11
        cpu.readOp()
        self.assertEqual(9, cpu.t_states)
