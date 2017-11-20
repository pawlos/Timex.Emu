import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_cpl(unittest.TestCase):

	def test_cpl_inverts_a(self):
		cpu = CPU(FakeRom('\x2f'), FakeRam())
		cpu.A = 0b10110100
		cpu.readOp();
		self.assertEqual(0b01001011, cpu.A)

