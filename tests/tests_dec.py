import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_b_sets_correct_value_is_set(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x01
		cpu.readOp();
		self.assertEqual(0x00, cpu.B)

	def test_dec_b_sets_z_flag_if_value_is_zero(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x01
		cpu.readOp();
		self.assertTrue(cpu.ZFlag)

	def test_dec_b_resets_z_flag_if_value_is_non_zero(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x00
		cpu.readOp();
		self.assertFalse(cpu.ZFlag)

	def test_dec_b_sets_s_flag_if_value_is_negative(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x00
		cpu.readOp();
		self.assertTrue(cpu.SFlag)

	def test_dec_b_resets_s_flag_if_value_is_positive(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x02
		cpu.readOp();
		self.assertFalse(cpu.SFlag)

	def test_dec_b_sets_n_flag(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x02
		cpu.NFlag = False
		cpu.readOp();
		self.assertTrue(cpu.NFlag)

	def test_dec_b_sets_PV_flag_if_borrow(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0b00010000
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_dec_c_sets_correct_value(self):
		cpu = CPU(FakeRom('\x0D'), FakeRam())
		cpu.C = 10
		cpu.readOp();
		self.assertEqual(9, cpu.C)

	def test_dec_d_sets_correct_value(self):
		cpu = CPU(FakeRom('\x15'), FakeRam())
		cpu.D = 0xFF
		cpu.readOp()
		self.assertEqual(0xFE, cpu.D)
