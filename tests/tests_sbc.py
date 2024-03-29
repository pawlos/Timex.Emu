import tests_suite

import unittest
from cpu import CPU
from rom import ROM
from utility import Bits


class tests_sbc(unittest.TestCase):

    def test_sbc_hl_hl_result_is_correct_if_c_flag_is_reset(self):
        cpu = CPU(ROM(b'\xed\x62'))
        cpu.HL = 0x9999
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x0, cpu.HL)

    def test_sbc_hl_sp_result_is_crrect_if_c_flag_is_reset(self):
        cpu = CPU(ROM(b'\xed\x72'))
        cpu.HL = 0x9999
        cpu.SP = 0x1111
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x8888, cpu.HL)

    def test_sbc_hl_de_result_is_correct_if_c_flag_is_set(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x9999
        cpu.DE = 0x1111
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(0x8887, cpu.HL)

    def test_sbc_hl_bc_result_is_crrect_if_c_flag_is_reset(self):
        cpu = CPU(ROM(b'\xed\x42'))
        cpu.HL = 0x9999
        cpu.BC = 0x1111
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x8888, cpu.HL)

    def test_sbc_hl_de_sets_n_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x9999
        cpu.DE = 0x1223
        cpu.NFlag = False
        cpu.readOp()
        self.assertTrue(cpu.NFlag)

    def test_sbc_hl_de_that_results_zero_sets_z_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x9999
        cpu.DE = 0x9999
        cpu.ZFlag = False
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_sbc_hl_de_that_results_non_zero_resets_z_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x9999
        cpu.DE = 0x9999
        cpu.CFlag = True
        cpu.ZFlag = True
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_sbc_hl_de_that_does_not_generate_carry_on_12bit_resets_h_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x0910
        cpu.DE = 0x0100
        cpu.HFlag = True
        cpu.readOp()
        self.assertFalse(cpu.HFlag)

    def test_sbc_hl_de_that_does_generate_carry_on_12th_bit_set_h_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x1000
        cpu.DE = 0x0001
        cpu.HFlag = False
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_sbc_hl_de_that_does_generate_borrow_sets_c_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x1000
        cpu.DE = 0x2000
        cpu.CFlag = False
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_sbc_hl_de_that_does_not_generate_borrow_resets_c_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x1000
        cpu.DE = 0x0999
        cpu.CFlag = True
        cpu.readOp()
        self.assertFalse(cpu.CFlag)

    def test_sbc_hl_de_that_results_in_value_less_than_zero_set_s_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x1000
        cpu.DE = 0x1002
        cpu.SFlag = False
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_sbc_hl_de_that_results_in_value_greater_than_zero_resets_s_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x1000
        cpu.DE = 0x0999
        cpu.SFLag = True
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_sbc_hl_de_that_overflows_sets_pv_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x8000
        cpu.DE = 0x1111
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)

    def test_sbc_hl_de_that_does_not_overflows_resets_pv_flag(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0xaaaa
        cpu.DE = 0xbbbb
        cpu.PVFlag = True
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)

    def test_sbc_hl_de_for_negative_values(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x3fff
        cpu.DE = 0xffff
        cpu.readOp()
        self.assertEqual(0x4000, cpu.HL)

    def test_sbc_hl_de_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x3fff
        cpu.DE = 0xffff
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_sbc_hl_de_takes_15_t_states(self):
        cpu = CPU(ROM(b'\xed\x52'))
        cpu.HL = 0x3fff
        cpu.DE = 0xffff
        cpu.readOp()
        self.assertEqual(15, cpu.t_states)

    def test_sbc_a_b_correctly_calculates_result(self):
        cpu = CPU(ROM(b'\x98'))
        cpu.A = 0x40
        cpu.B = 0x3f
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0, cpu.A)

    def test_sbc_a_c_without_c_calculates_results(self):
        cpu = CPU(ROM(b'\x99'))
        cpu.A = 0x40
        cpu.C = 0x3f
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(1, cpu.A)

    def test_sbc_a_d_sets_SFlag_when_result_is_below_zero(self):
        cpu = CPU(ROM(b'\x9a'))
        cpu.A = 0x40
        cpu.D = 0x44
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_sbc_a_e_sets_ZFlag_when_result_is_zero(self):
        cpu = CPU(ROM(b'\x9b'))
        cpu.A = 0x44
        cpu.E = 0x44
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_sbc_a_mem_hl_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\x9e\x00\x00\x22'))
        cpu.A = 0x23
        cpu.HL = 0x3
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0, cpu.A)
