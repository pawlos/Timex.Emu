import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestSBC(unittest.TestCase):

	def test_sbc_hl_de_result_is_correct_if_c_flag_is_set(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x1111
		cpu.CFlag = True
		cpu.readOp();
		self.assertEqual(0x8887, cpu.HL)

	def test_sbc_hl_de_result_is_crrect_if_c_flag_is_reset(self):
		cpu = CPU(FakeRom('\xed\x52'))
		cpu.HL = 0x9999
		cpu.DE = 0x1111
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