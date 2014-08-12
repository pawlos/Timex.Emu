import unittest
from cpu import CPU
from fakes import *

class TestInc(unittest.TestCase):
	def test_inc_hl_does_add_1_to_hl_value(self):
		cpu = CPU(FakeRom('\x23'))
		cpu.HL = 0xfff
		cpu.readOp()
		self.assertEqual(0x1000, cpu.HL)