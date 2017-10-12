import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_ix_nn(unittest.TestCase):
	''' DD 2A n n '''
	def test_ld_ix_nn_correctly_copies_nn_value_to_ix(self):
		ram = FakeRam([None]*0x6668)
		ram.storeAddr(0x6666, 0x92)
		ram.storeAddr(0x6667, 0xDA)
		cpu = CPU(FakeRom('\xDD\x2A\x66\x66'), ram)
		cpu.readOp()
		self.assertEqual(0xDA92, cpu.IX)
