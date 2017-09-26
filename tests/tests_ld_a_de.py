import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestLDADE(unittest.TestCase):

	def test_ld_a_de_loads_corect_value(self):
		ram = FakeRam([0x00]*0x5000)
		ram.storeAddr(0x30A2, 0x22)
		cpu = CPU(FakeRom('\x1a'), ram)
		cpu.DE = 0x30A2
		cpu.readOp();
		self.assertEqual(0x22, cpu.A)