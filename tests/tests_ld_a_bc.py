import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestLDABC(unittest.TestCase):

	def test_ld_a_bc_loads_corect_value(self):
		ram = FakeRam([0x00]*0x5000)
		ram.storeAddr(0x4747, 0x12)
		cpu = CPU(FakeRom('\x0a'), ram)
		cpu.BC = 0x4747
		cpu.readOp();
		self.assertEqual(0x12, cpu.A)