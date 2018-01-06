import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_and_n(unittest.TestCase):
	def test_and_n_performs_and_operation(self):
		cpu = CPU(FakeRom('\xe6\x10'))
		cpu.A = 0x01
		cpu.readOp()
		self.assertEqual(0x0, cpu.A)
