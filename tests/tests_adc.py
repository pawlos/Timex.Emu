import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import *

class tests_adc(unittest.TestCase):

	def test_add_HL_BC_with_C_flag_unset_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x4a'))
		cpu.HL = 0xCDCD
		cpu.BC = 0x1111
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111,cpu.HL)


	def test_add_HL_BC_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x4a'))
		cpu.HL = 0xCDCD
		cpu.BC = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111+0x1,cpu.HL)

	def test_add_HL_DE_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x5a'))
		cpu.HL = 0xCDCD
		cpu.DE = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111+0x1,cpu.HL)

	def test_add_HL_HL_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x6a'))
		cpu.HL = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x1111+0x1111+0x1,cpu.HL)

	def test_add_HL_SP_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x7a'))
		cpu.HL = 0x1111
		cpu.SP = 0x2222
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x1111+0x2222+0x1,cpu.HL)

	def test_add_a_b_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\x88'))
		cpu.A = 0x12
		cpu.B = 0x12
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x25, cpu.A)

	def test_add_a_b_with_C_flag_reset_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\x88'))
		cpu.A = 0x22
		cpu.B = 0x33
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x55, cpu.A)

	def test_add_a_c_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x89'))
		cpu.A = 0x22
		cpu.C = 0x88
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0xAB, cpu.A)

	def test_add_a_c_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x89'))
		cpu.A = 0x22
		cpu.C = 0x88
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0xAA, cpu.A)

	def test_add_a_d_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8a'))
		cpu.A = 0x22
		cpu.D = 0x77
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x9a, cpu.A)

	def test_add_a_d_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8a'))
		cpu.A = 0x22
		cpu.D = 0x77
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x99, cpu.A)

	def test_add_a_e_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8b'))
		cpu.A = 0x22
		cpu.E = 0x66
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x89, cpu.A)

	def test_add_a_e_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8b'))
		cpu.A = 0x22
		cpu.E = 0x66
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x88, cpu.A)

	def test_add_a_h_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8c'))
		cpu.A = 0x22
		cpu.H = 0x55
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x78, cpu.A)

	def test_add_a_h_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8c'))
		cpu.A = 0x22
		cpu.H = 0x55
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x77, cpu.A)

	def test_add_a_l_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8d'))
		cpu.A = 0x22
		cpu.L = 0x44
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x67, cpu.A)

	def test_add_a_l_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8d'))
		cpu.A = 0x22
		cpu.L = 0x44
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x66, cpu.A)

	def test_add_a_a_with_C_flag_set_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8f'))
		cpu.A = 0x22
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x45, cpu.A)

	def test_add_a_a_with_C_flag_reset_correctly_caluclates_value(self):
		cpu = CPU(FakeRom('\x8f'))
		cpu.A = 0x22
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x44, cpu.A)

	def test_add_a_a_with_C_flag_reset_correctly_sets_ZFlag(self):
		cpu = CPU(FakeRom('\x8f'))
		cpu.A = 0x00
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_add_a_a_with_C_flag_set_correctly_resets_ZFlag(self):
		cpu = CPU(FakeRom('\x8f'))
		cpu.A = 0x00
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)