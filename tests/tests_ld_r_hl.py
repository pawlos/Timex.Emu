import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_r_hl(unittest.TestCase):
	
	def test_ld_b_hl_correctly_copies_value_to_b(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af, 0x39)
		cpu = CPU(FakeRom('\x46'), ram)
		cpu.HL = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.B)
