import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class or_a(unittest.TestCase):
	def test_or_a_performs_or_operation_value_is_correct(self):
		cpu = CPU(FakeRom('\xf6\x48'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(0x5A, cpu.A)

	def test_or_a_performs_or_operation_Z_is_set_when_value_is_zero(self):
		cpu = CPU(FakeRom('\xf6\x00'))
		cpu.ZFlag = False
		cpu.A = 0x00
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_or_a_performs_or_operation_S_is_set_when_value_is_negative(self):
		cpu = CPU(FakeRom('\xf6\x00'))
		cpu.SFlag = False
		cpu.A = 0xCD
		cpu.readOp()
		self.assertTrue(cpu.SFlag)