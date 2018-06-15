import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class test_ld_de_a(unittest.TestCase):

	def test_ld_de_a_loads_corect_value(self):
		ram = FakeRam([0x00]*0x1130)
		cpu = CPU(FakeRom('\x12'), ram)
		cpu.A = 0xA0
		cpu.DE = 0x1128
		cpu.readOp()
		self.assertEqual(0xA0, cpu.ram.readAddr(cpu.DE))