import unittest
from cpu import CPU
from fakes import *

class TestInc(unittest.TestCase):
	def test_inc_hl_does_add_1_to_hl_value(self):
		cpu = CPU(FakeRom('\x23'))
		cpu.HL = 0xfff
		cpu.readOp()
		self.assertEqual(0x1000, cpu.HL)

	def test_inc_hl_does_not_affect_c_flag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xfff
		cpu.CFlag = True
		cpu.readOp()
		self.assertTrue(cpu.CFlag)
		cpu.CFlag = False
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_inc_hl_does_not_affect_z_flag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xffff
		cpu.ZFlag = True
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)
		cpu.ZFlag = False
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_inc_hl_does_not_affect_pv_flag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xfff
		cpu.PVFlag = True
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)
		cpu.PVFlag = False
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)

	def test_inc_hl_does_not_affect_n_hlag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xfff
		cpu.NFlag = True
		cpu.readOp()
		self.assertTrue(cpu.NFlag)
		cpu.NFlag = False
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_inc_hl_does_not_affect_s_hlag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xfff
		cpu.SFlag = True
		cpu.readOp()
		self.assertTrue(cpu.SFlag)
		cpu.SFlag = False
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_inc_hl_does_not_affect_h_hlag(self):
		cpu = CPU(FakeRom('\x23\x23'))
		cpu.HL = 0xfff
		cpu.HFlag = True
		cpu.readOp()
		self.assertTrue(cpu.HFlag)
		cpu.HFlag = False
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_inc_r_correctly_adds_one(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.B = 0
		cpu.readOp()
		self.assertEqual(1, cpu.B)

	def test_inc_r_does_reset_N_flag(self):
		cpu = CPU(FakeRom('\x04\x04'))
		cpu.B = 0xAA
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.NFlag)
		cpu.NFlag = False #redundant but to be explicit
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_inc_r_does_not_affect_C_flag(self):
		cpu = CPU(FakeRom('\x04\x04'))
		cpu.B = 0xCB
		cpu.CFlag = True
		cpu.readOp()
		self.assertTrue(cpu.CFlag)
		cpu.readOp()
		cpu.CFlag = False
		self.assertFalse(cpu.CFlag)

	def test_inc_r_does_reset_Z_flag_when_result_is_non_zero(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.B = 0;
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_inc_r_set_Z_flag_when_result_is_zero(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.B = 0xff
		cpu.ZFlag = False
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_inc_r_set_H_flag_if_bit_no_3_is_set(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.B = 0x07
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_inc_r_reset_H_flag_if_bit_no_3_is_reset(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.B = 0x0f
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)
