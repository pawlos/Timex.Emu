import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_jpc(unittest.TestCase):

	def test_jp_c_jumps_if_CFlag_is_set(self):
		rom = '\x00' * 0x480+'\x38\x00'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x480
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0x480, cpu.PC)

	def test_jp_c_does_not_jump_if_CFlag_is_reset(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)

	def test_jp_c_does_take_2_m_cycles_if_condition_is_not_met(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_jp_c_does_take_7_t_states_if_condition_is_not_met(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_jp_c_does_take_3_m_cycles_if_condition_is_met(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_jp_c_does_take_12_t_states_if_condition_is_met(self):
		cpu = CPU(FakeRom('\x38\x00'))
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(12, cpu.t_states)