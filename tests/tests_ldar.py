import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ldar(unittest.TestCase):

	def test_ldar_copies_correct_value_from_R_to_A(self):
		cpu = CPU(FakeRom('\xed\x5f'))
		cpu.R = 0x11
		cpu.readOp();
		self.assertEqual(0x11, cpu.A)