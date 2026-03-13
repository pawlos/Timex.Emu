import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_missing_timing(unittest.TestCase):

    def test_inc_ix_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xdd\x23'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_inc_ix_takes_10_t_states(self):
        cpu = CPU(ROM(b'\xdd\x23'))
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)

    def test_inc_iy_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xfd\x23'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_inc_iy_takes_10_t_states(self):
        cpu = CPU(ROM(b'\xfd\x23'))
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)

    def test_sub_n_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xd6\x01'))
        cpu.A = 0x05
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_sub_n_takes_7_t_states(self):
        cpu = CPU(ROM(b'\xd6\x01'))
        cpu.A = 0x05
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_ld_r_ix_d_takes_5_m_cycles(self):
        ram = RAM()
        ram[0x1001] = 0x42
        cpu = CPU(ROM(b'\xdd\x46\x01'), ram)
        cpu.IX = 0x1000
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_r_ix_d_takes_19_t_states(self):
        ram = RAM()
        ram[0x1001] = 0x42
        cpu = CPU(ROM(b'\xdd\x46\x01'), ram)
        cpu.IX = 0x1000
        cpu.readOp()
        self.assertEqual(19, cpu.t_states)

    def test_ld_at_ix_d_r_takes_5_m_cycles(self):
        cpu = CPU(ROM(b'\xdd\x70\x01'))
        cpu.IX = 0x1000
        cpu.B = 0x42
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_at_ix_d_r_takes_19_t_states(self):
        cpu = CPU(ROM(b'\xdd\x70\x01'))
        cpu.IX = 0x1000
        cpu.B = 0x42
        cpu.readOp()
        self.assertEqual(19, cpu.t_states)

    def test_ld_at_ix_d_nn_takes_5_m_cycles(self):
        cpu = CPU(ROM(b'\xdd\x36\x01\x42'))
        cpu.IX = 0x1000
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_at_ix_d_nn_takes_19_t_states(self):
        cpu = CPU(ROM(b'\xdd\x36\x01\x42'))
        cpu.IX = 0x1000
        cpu.readOp()
        self.assertEqual(19, cpu.t_states)

    def test_adc_n_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xce\x01'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_adc_n_takes_7_t_states(self):
        cpu = CPU(ROM(b'\xce\x01'))
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_daa_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\x27'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_daa_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x27'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
