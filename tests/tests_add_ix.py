import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_add_ix(unittest.TestCase):

	def test_add_ix_bc_returns_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x09'))
		cpu.IX = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IX)

	def test_add_ix_bc_returns_correct_result(self):
		cpu = CPU(FakeRom('\xdd\x19'))
		cpu.IX = 0x1001
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IX)
