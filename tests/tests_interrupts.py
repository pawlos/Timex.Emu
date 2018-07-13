import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_interrupts(unittest.TestCase):
	def test_di(self):
		cpu = CPU(ROM('\xf3'))
		cpu.readOp()

		self.assertEqual(0x00, cpu.iff1)

	def test_di_(self):
		cpu = CPU(ROM('\xfb'))
		cpu.readOp()

		self.assertEqual(0x01, cpu.iff1)