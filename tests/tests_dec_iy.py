import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_iy_sets_correct_value_is_set(self):
		ram = RAM()
		ram[0x10f] = 0xDD
		cpu = CPU(FakeRom('\xfd\x35\x0f'), ram)
		cpu.IY = 0x100
		cpu.readOp()
		self.assertEqual(0xDC, ram[cpu.IY+15])

