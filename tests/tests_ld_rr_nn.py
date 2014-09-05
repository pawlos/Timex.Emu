import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_rr_nn(unittest.TestCase):

	def test_ld_BC_nn_correctly_stores_value_to_register(self):
		cpu = CPU(FakeRom('\x01\xba\xab'))
		cpu.readOp()
		self.assertEqual(0xabba, cpu.BC)

	def test_ld_hl_nn_correctly_stores_value_to_hl(self):
		cpu = CPU(FakeRom('\x21\xfe\xca'))
		cpu.readOp()
		self.assertEqual(0xcafe, cpu.HL)
