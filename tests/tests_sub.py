import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestSUB(unittest.TestCase):

	def test_sub_n_set_corrects_value(self):
		cpu = CPU(FakeRom('\xd6\x52'))
		cpu.A = 0x52
		cpu.readOp();
		self.assertEqual(0x00, cpu.A)

	def test_sub_n_set_ZFlag_if_value_is_zero(self):
		cpu = CPU(FakeRom('\xd6\x52'))
		cpu.A = 0x52
		cpu.readOp();
		self.assertTrue(cpu.ZFlag)

