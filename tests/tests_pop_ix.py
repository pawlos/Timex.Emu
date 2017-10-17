import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class pop(unittest.TestCase):

	def test_pop_ix_correctly_retreives_value_from_stack(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xdd\xe1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.IX)

	