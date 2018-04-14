import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_sbc(unittest.TestCase):

	def test_sbc_hl_hl_result_is_correct_if_c_flag_is_reset(self):
		cpu = CPU(FakeRom('\xed\x62'))
		cpu.HL = 0x9999
		cpu.CFlag = False
		cpu.readOp();
		self.assertEqual(0x0, cpu.HL)

	def test_sbc_hl_sp_result_is_crrect_if_c_flag_is_reset(self):
		cpu = CPU(FakeRom('\xed\x72'))
		cpu.HL = 0x9999
		cpu.SP = 0x1111
		cpu.CFlag = False
		cpu.readOp();
		self.assertEqual(0x8888, cpu.HL)

	def test_sbc_hl_de_result_is_correct_if_c_flag_is_set(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x1111
		cpu.CFlag = True
		cpu.readOp();
		self.assertEqual(0x8887, cpu.HL)

	def test_sbc_hl_bc_result_is_crrect_if_c_flag_is_reset(self):
		cpu = CPU(FakeRom('\xed\x42'))
		cpu.HL = 0x9999
		cpu.BC = 0x1111
		cpu.CFlag = False
		cpu.readOp();
		self.assertEqual(0x8888, cpu.HL)

	def test_sbc_hl_de_sets_n_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x1223
		cpu.NFlag = False
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_sbc_hl_de_that_results_zero_sets_z_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x9999
		cpu.ZFlag = False
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_sbc_hl_de_that_results_non_zero_resets_z_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x9999
		cpu.CFlag = True
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_sbc_hl_de_that_results_in_borrow_sets_h_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x0800
		cpu.DE = 0x0
		cpu.CFlag = True
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_sbc_hl_de_that_does_not_generate_carry_on_12bit_resets_h_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x0910
		cpu.DE = 0x0100
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_sbc_hl_de_that_does_generate_carry_on_12th_bit_set_h_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1000
		cpu.DE = 0x0001
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_sbc_hl_de_that_does_generate_borrow_sets_c_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1000
		cpu.DE = 0x2000
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_sbc_hl_de_that_does_not_generate_borrow_resets_c_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1000
		cpu.DE = 0x0999
		cpu.CFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_sbc_hl_de_that_results_in_value_less_than_zero_set_s_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1000
		cpu.DE = 0x1002
		cpu.SFLag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_sbc_hl_de_that_results_in_value_greater_than_zero_resets_s_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1000
		cpu.DE = 0x0999
		cpu.SFLag = True
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_sbc_hl_de_that_overflows_sets_pv_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x1111
		cpu.DE = 0x8000
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_sbc_hl_de_that_does_not_overflows_resets_pv_flag(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0xaaaa
		cpu.DE = 0xbbbb
		cpu.PVFlag = True
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)


	def test_sbc_hl_de_for_negative_values(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x3fff
		cpu.DE = 0xffff
		cpu.readOp()
		self.assertEquals(0x4000, cpu.HL)

	def test_sbc_hl_de_takes_4_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x3fff
		cpu.DE = 0xffff
		cpu.readOp()
		self.assertEquals(4, cpu.m_cycles)

	def test_sbc_hl_de_takes_15_t_states(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x3fff
		cpu.DE = 0xffff
		cpu.readOp()
		self.assertEquals(15, cpu.t_states)