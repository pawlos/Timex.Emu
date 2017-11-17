import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_hl_sets_correct_value_is_set(self):
		ram = FakeRam([None]*0x200)
		ram.storeAddr(0x100, 0xDD)
		cpu = CPU(FakeRom('\x35'), ram)
		cpu.HL = 0x100
		cpu.readOp();
		self.assertEqual(0xDC, ram.readAddr(cpu.HL))

