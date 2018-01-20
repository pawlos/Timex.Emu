import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ldra(unittest.TestCase):

	def test_ldra_does_copy_value_correctly_from_A_to_R(self):
		cpu = CPU(FakeRom('\xed\x4f'))
		cpu.A = 0b01110110
		cpu.readOp();
		self.assertEqual(0b01110110, cpu.R)