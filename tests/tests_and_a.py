import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class and_a(unittest.TestCase):
	def test_and_a_performs_and_operation(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(0x12, cpu.A)

	def test_and_a_sets_HFlag(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.A = 0x12
		cpu.HFlag = False
		cpu.readOp();
		self.assertTrue(cpu.HFlag)

	def test_and_a_resets_n_and_c_flag(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.CFlag = True
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)
		self.assertFalse(cpu.NFlag)