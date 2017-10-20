import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_jp_cond(unittest.TestCase):

	def test_jp_c_jumps_if_ZFlag_is_set(self):
		cpu = CPU(FakeRom('\xDA\x20\x15'))
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_c_not_does_jump_if_ZFlag_is_not_set(self):
		cpu = CPU(FakeRom('\xDA\x20\x15'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(0x03, cpu.PC)