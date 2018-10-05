import unittest
from cpu import CPU
from rom import ROM


class tests_cpl(unittest.TestCase):

    def test_cpl_inverts_a(self):
        cpu = CPU(ROM('\x2f'))
        cpu.A = 0b10110100
        cpu.readOp()
        self.assertEqual(0b01001011, cpu.A)

    def test_cpl_takes_1_m_cycles(self):
        cpu = CPU(ROM('\x2f'))
        cpu.A = 0b10110100
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_cpl_takes_4_t_states(self):
        cpu = CPU(ROM('\x2f'))
        cpu.A = 0b10110100
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
