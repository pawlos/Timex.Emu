import unittest
from cpu import CPU
from rom import ROM


class tests_ccf(unittest.TestCase):

    def test_ccf_inverts_c(self):
        cpu = CPU(ROM(b'\x3f'))
        cpu.CFlag = True
        cpu.readOp()
        self.assertFalse(cpu.CFlag)

    def test_ccf_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\x3f'))
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ccf_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x3f'))
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
