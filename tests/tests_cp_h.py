import unittest

from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_cp_h(unittest.TestCase):

	def test_cp_H_sets_ZF_if_H_is_equal_to_0(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 3
		cpu.H = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_B(self):
		cpu = CPU(ROM('\xb8'))
		cpu.A = 3
		cpu.B = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_C(self):
		cpu = CPU(ROM('\xb9'))
		cpu.A = 3
		cpu.C = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_D(self):
		cpu = CPU(ROM('\xba'))
		cpu.A = 3
		cpu.D = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_E(self):
		cpu = CPU(ROM('\xbb'))
		cpu.A = 3
		cpu.E = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_L(self):
		cpu = CPU(ROM('\xbd'))
		cpu.A = 3
		cpu.L = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_A(self):
		cpu = CPU(ROM('\xbf'))
		cpu.A = 5
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_H_resets_ZF_if_H_is_not_equal_to_0(self):
		cpu = CPU(ROM('\xbc'))
		cpu.H = 1
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_cp_H_sets_SF_if_H_is_negative(self):
		cpu = CPU(ROM('\xbc'))
		cpu.H = 1
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_H_sets_NF_always(self):
		cpu = CPU(ROM('\xbc'))
		cpu.H = 0
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_cp_H_sets_CF_is_results_goes_below_zero(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 3
		cpu.H = 0xff
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_cp_H_sets_HF(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 0x10
		cpu.H = 0x01
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_cp_H_resets_HF(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 0x3
		cpu.H = 0x1
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_cp_H_sets_PVF(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 0x7f
		cpu.H = 0x81
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_cp_H_sets_SF_if_value_is_negative(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 1
		cpu.H = 3
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_H_sets_CF_if_borrow(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 1
		cpu.H = 3
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_cp_r_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 3
		cpu.H = 3
		cpu.readOp()
		self.assertEquals(1, cpu.m_cycles)

	def test_cp_r_takes_4_t_states(self):
		cpu = CPU(ROM('\xbc'))
		cpu.A = 3
		cpu.H = 3
		cpu.readOp()
		self.assertEquals(4, cpu.t_states)

	def test_cp_hl_sets_ZFlag_correctly(self):
		cpu = CPU(ROM('\xbe\x01\x02\x04\x03'))
		cpu.A = 0x3
		cpu.HL = 0x04
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_hl_sets_SFlag_correctly(self):
		cpu = CPU(ROM('\xbe\x01\x02\x04\x05'))
		cpu.A = 0x03
		cpu.HL = 0x03
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_hl_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xbe\x01\x02\x04\x05'))
		cpu.A = 0x03
		cpu.HL = 0x03
		cpu.readOp()
		self.assertEquals(1, cpu.m_cycles)

	def test_cp_hl_takes_7_t_states(self):
		cpu = CPU(ROM('\xbe\x01\x02\x04\x05'))
		cpu.A = 0x03
		cpu.HL = 0x03
		cpu.readOp()
		self.assertEquals(7, cpu.t_states)