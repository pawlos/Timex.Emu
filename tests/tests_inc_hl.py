import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_inc(unittest.TestCase):

	def test_inc_hl_sets_correct_value_is_set(self):
		ram = FakeRam([None]*0x200)
		ram.storeAddr(0x100, 0xDD)
		cpu = CPU(FakeRom('\x34'), ram)
		cpu.HL = 0x100
		cpu.readOp();
		self.assertEqual(0xDE, ram.readAddr(cpu.HL))


