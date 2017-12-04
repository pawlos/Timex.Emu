import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_add_ix(unittest.TestCase):

	def test_add_ix_bc_returns_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x09'))
		cpu.IX = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IX)

	def test_add_ix_de_returns_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x19'))
		cpu.IX = 0x1001
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IX)

	def test_add_ix_ix_returns_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x29'))
		cpu.IX = 0x1001
		cpu.readOp()
		self.assertEqual(0x2002, cpu.IX)

	def test_add_ix_sp_retursn_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x39'))
		cpu.IX = 0x1001
		cpu.SP = 0x0880
		cpu.readOp()
		self.assertEqual(0x1881, cpu.IX)

	def test_add_ix_rr_resets_n_flag(self):
		cpu = CPU(FakeRom('\xdd\x39'))
		cpu.IX = 0x1001
		cpu.SP = 0x0880
		cpu.NFlag = Bits.set()
		cpu.readOp()
		self.assertFalse(cpu.NFlag)
