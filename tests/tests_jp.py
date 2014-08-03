import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class jp(unittest.TestCase):

	def test_jp_nz_jumps_if_ZFlag_is_non_zero(self):
		rom = [None] * 0x0482
		rom[0x480] = '\x20'
		rom[0x481] = '\xFA'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x0480
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x047C, cpu.PC)

	def test_jp_nz_does_not_jump_if_ZFlag_is_set(self):
		cpu = CPU(FakeRom('\x20\xFA'))
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)