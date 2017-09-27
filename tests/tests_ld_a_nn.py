import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestLDAnn(unittest.TestCase):

	def test_ld_a_nn_loads_corect_value(self):
		ram = FakeRam([0x00]*0x8833)
		ram.storeAddr(0x8832, 0x04)
		cpu = CPU(FakeRom('\x3a\x32\x88'), ram)
		cpu.readOp();
		self.assertEqual(0x4, cpu.A)