import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *

class tests_jrz(unittest.TestCase):

	def test_jr_z_jumps_if_ZFlag_is_set(self):
		rom = '\x00' * 0x0300+'\x28\x03'
		cpu = CPU(FakeRom(rom), FakeRam())
		cpu.PC = 0x0300
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x0305, cpu.PC)

	def test_jr_z_does_not_jump_if_ZFlag_is_reset(self):
		cpu = CPU(FakeRom('\x28\x00'), FakeRam())
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)

	def test_jr_z_does_not_change_the_z_flag(self):
		cpu = CPU(FakeRom('\x28\x00\x28\x00'))
		cpu.ZFlag = False
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)
		cpu.ZFlag = True
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)