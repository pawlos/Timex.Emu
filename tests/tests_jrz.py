import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *

class jrz(unittest.TestCase):

	def test_jr_z_jumps_if_ZFlag_is_set(self):
		rom = [None] * 0x0302
		rom[0x300] = '\x28'
		rom[0x301] = '\x03'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x0300
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x0305, cpu.PC)

	def test_jr_z_does_not_jump_if_ZFlag_is_reset(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)