import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_interrupts(unittest.TestCase):
	def test_di(self):
		cpu = CPU(FakeRom('\xf3'))
		cpu.readOp()

		self.assertEqual(0x00, cpu.iff)

	def test_di_(self):
		cpu = CPU(FakeRom('\xfb'))
		cpu.readOp()

		self.assertEqual(0x01, cpu.iff)