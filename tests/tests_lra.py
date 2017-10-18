import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_lra(unittest.TestCase):

	def test_lra_does_modify_value_correctly(self):
		cpu = CPU(FakeRom('\x17'))
		cpu.A = 0b01110110
		cpu.CFlag = True
		cpu.readOp();
		self.assertEqual(0b11101101, cpu.A)
		self.assertFalse(cpu.CFlag)