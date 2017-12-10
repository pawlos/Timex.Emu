import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_add_iy(unittest.TestCase):

	def test_add_iy_bc_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x09'))
		cpu.IY = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IY)

	def test_add_iy_de_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x19'))
		cpu.IY = 0x1001
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IY)

	def test_add_iy_iy_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x29'))
		cpu.IY = 0x1001
		cpu.readOp()
		self.assertEqual(0x2002, cpu.IY)

	def test_add_iy_sp_retursn_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IY = 0x1001
		cpu.SP = 0x0880
		cpu.readOp()
		self.assertEqual(0x1881, cpu.IY)

	'''def test_add_iy_rr_resets_n_flag(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IX = 0x1001
		cpu.SP = 0x0880
		cpu.NFlag = Bits.set()
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_add_iy_rr_sets_c_flag_is_results_is_too_big(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IX = 0xFFFF
		cpu.SP = 0x0001
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_ix_rr_sets_h_flag_if_carry_from_11th_bit(self):
		cpu = CPU(FakeRom('\xdd\x39'))
		cpu.IX = 0xFFF
		cpu.SP = 0x0001
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)'''
