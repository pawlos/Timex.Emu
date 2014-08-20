import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_nn_rr(unittest.TestCase):

	def test_ed43nn_correctly_stores_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x43\x10\0x00'))
		cpu.BC = 0x4644
		cpu.readOp()
		self.assertEqual(cpu.ram.readAddr(0x1000), 0x46)
		self.assertEqual(cpu.ram.readAddr(0x1001), 0x44)