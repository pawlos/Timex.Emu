import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_iy_r(unittest.TestCase):
	
	def test_ld_iy_d_l_correctly_copies_value_to_memory(self):
		ram = FakeRam([None]*0x2600)
		cpu = CPU(FakeRom('\xFD\x75\x10'), ram)
		cpu.IY = 0x25AF
		cpu.L = 0x39
		cpu.readOp()
		self.assertEqual(0x39, ram.readAddr(0x25bf))