import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from rom import ROM
from utility import Bits


class tests_add_ix(unittest.TestCase):

    def test_add_ix_bc_returns_correct_result(self):
        cpu = CPU(ROM(b'\xdd\x09'))
        cpu.IX = 0x1001
        cpu.BC = 0x0bb0
        cpu.readOp()
        self.assertEqual(0x1bb1, cpu.IX)

    def test_add_ix_de_returns_correct_result(self):
        cpu = CPU(ROM(b'\xdd\x19'))
        cpu.IX = 0x1001
        cpu.DE = 0x0bb0
        cpu.readOp()
        self.assertEqual(0x1bb1, cpu.IX)

    def test_add_ix_ix_returns_correct_result(self):
        cpu = CPU(ROM(b'\xdd\x29'))
        cpu.IX = 0x1001
        cpu.readOp()
        self.assertEqual(0x2002, cpu.IX)

    def test_add_ix_sp_returns_correct_result(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0x1001
        cpu.SP = 0x0880
        cpu.readOp()
        self.assertEqual(0x1881, cpu.IX)

    def test_add_ix_rr_resets_n_flag(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0x1001
        cpu.SP = 0x0880
        cpu.NFlag = Bits.set()
        cpu.readOp()
        self.assertFalse(cpu.NFlag)

    def test_add_ix_rr_sets_c_flag_is_results_is_too_big(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0xFFFF
        cpu.SP = 0x0001
        cpu.CFlag = False
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_add_ix_rr_sets_h_flag_if_carry_from_11th_bit(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0xFFF
        cpu.SP = 0x0001
        cpu.HFlag = False
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_add_ix_rr_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0xFFF
        cpu.SP = 0x0001
        cpu.HFlag = False
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_add_ix_rr_takes_15_t_states(self):
        cpu = CPU(ROM(b'\xdd\x39'))
        cpu.IX = 0xFFF
        cpu.SP = 0x0001
        cpu.HFlag = False
        cpu.readOp()
        self.assertEqual(15, cpu.t_states)
