import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class test_ld_a_bc_loads_corect_value(unittest.TestCase):

	def test_ld_bc_a_loads_corect_value(self):
		ram = FakeRam([0x00]*0x1214)
		cpu = CPU(FakeRom('\x02'), ram)
		cpu.A = 0x7a
		cpu.BC = 0x1212
		cpu.readOp();
		self.assertEqual(0x7a, cpu.ram.readAddr(cpu.BC))