import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from utility import Bits

class tests_jrz(unittest.TestCase):

	def test_jr_z_jumps_if_ZFlag_is_set(self):
		rom = '\x00' * 0x0300+'\x28\x03'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x0300
		cpu.ZFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x0305, cpu.PC)

	def test_jr_z_does_not_jump_if_ZFlag_is_reset(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)

	def test_jr_z_does_not_change_the_z_flag(self):
		cpu = CPU(FakeRom('\x28\x00\x28\x00'))
		cpu.ZFlag = Bits.reset()
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)
		cpu.ZFlag = Bits.set()
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_jr_z_takes_2_m_cycles_if_condition_is_not_met(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_jr_z_takes_7_t_states_if_condition_is_not_met(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_jr_z_takes_3_m_cycles_if_condition_is_met(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_jr_z_takes_12_t_states_if_condition_is_met(self):
		cpu = CPU(FakeRom('\x28\x00'))
		cpu.ZFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(12, cpu.t_states)
