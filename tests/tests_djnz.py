import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *

class tests_djnz(unittest.TestCase):

	def test_djnz_doesn_jumps_if_B_is_zero_after_dec(self):
		cpu = CPU(FakeRom('\x10\x02'))
		cpu.B = 1
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)
