import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_rra(unittest.TestCase):

	def test_rra_does_modify_value_correctly(self):
		cpu = CPU(FakeRom('\x1f'))
		cpu.A = 0b11100001
		cpu.CFlag = False
		cpu.readOp();
		self.assertEqual(0b01110000, cpu.A)
		self.assertTrue(cpu.CFlag)