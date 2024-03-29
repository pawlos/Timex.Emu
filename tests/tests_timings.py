import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_timings(unittest.TestCase):

    def test_ld16_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\x01'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld16_takes_10_t_states(self):
        cpu = CPU(ROM(b'\x01'))
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)

    def test_ld_bc_a_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\x02'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_bc_a_takes_7_t_states(self):
        cpu = CPU(ROM(b'\x02'))
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_ld_r_n_takes_2_m_cycle(self):
        cpu = CPU(ROM(b'\x06'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_r_n_takes_7_t_states(self):
        cpu = CPU(ROM(b'\x06'))
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_ei_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\xfb'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ei_takes_4_t_states(self):
        cpu = CPU(ROM(b'\xfb'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)

    def test_di_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\xf3'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_di_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\xf3'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
