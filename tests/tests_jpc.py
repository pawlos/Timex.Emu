import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_jpc(unittest.TestCase):

	def test_jp_c_jumps_if_CFlag_is_set(self):
		rom = [None] * 0x0482
		rom[0x480] = '\x38'
		rom[0x481] = '\x00'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x0480
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0x0480, cpu.PC)

	def test_jp_c_does_not_jump_if_CFlag_is_reset(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)