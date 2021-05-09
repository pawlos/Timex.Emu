import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_in(unittest.TestCase):
    def test_in_from_port_specified_in_c_puts_value_of_reg_A(self):
        cpu = CPU(ROM(b'\xed\x78'))
        cpu.C = 0x44
        cpu.io[cpu.C] = 0xAA

        cpu.readOp()
        self.assertEqual(0xAA, cpu.io[0x44])

    def test_in_from_port_takes_3_m_cycles(self):
        cpu = CPU(ROM(b'\xed\x78'))
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_in_from_port_takes_12_t_states(self):
        cpu = CPU(ROM(b'\xed\x78'))
        cpu.readOp()
        self.assertEqual(12, cpu.t_states)

    def test_in_A_n_correctly_reads_value_from_port_n(self):
        cpu = CPU(ROM(b'\xdb\x12'))
        cpu.io[0x12] = 0x55

        cpu.readOp()
        self.assertEqual(0x55, cpu.A)

    def test_in_A_n_takes_3_m_cycles(self):
        cpu = CPU(ROM(b'\xdb\x12'))
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_in_A_n_takes_11_t_states(self):
        cpu = CPU(ROM(b'\xdb\x12'))
        cpu.readOp()
        self.assertEqual(11, cpu.t_states)
