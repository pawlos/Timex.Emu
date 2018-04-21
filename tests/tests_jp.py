import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_jp(unittest.TestCase):

	def test_jp_nz_jumps_if_ZFlag_is_non_zero(self):
		rom = '\x00' * 0x0480+'\x20\xFA'
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


	def test_jp_hl_does_set_ip_to_value_of_hl(self):
		cpu = CPU(FakeRom('\xe9'))
		cpu.HL = 0x4800
		cpu.readOp()
		self.assertEqual(0x4800, cpu.PC)

	def test_jp_e_does_set_ip_to_value_of_e(self):
		cpu = CPU(FakeRom('\x00'*0x480+'\x18\x03'))
		cpu.PC = 0x480
		cpu.readOp()
		self.assertEqual(0x485, cpu.PC)

	def test_jp_ix_does_set_ip_to_value_of_ix(self):
		cpu = CPU(FakeRom('\xdd\xe9'))
		cpu.IX = 0x4600
		cpu.readOp()
		self.assertEqual(0x4600, cpu.PC)

	def test_jp_iy_does_set_ip_to_value_of_iy(self):
		cpu = CPU(FakeRom('\xfd\xe9'))
		cpu.IY = 0x4622
		cpu.readOp()
		self.assertEqual(0x4622, cpu.PC)

	def test_jr_e_takes_3_m_cycles(self):
		cpu = CPU(FakeRom('\x00'*0x480+'\x18\x03'))
		cpu.PC = 0x480
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_jr_e_takes_12_t_states(self):
		cpu = CPU(FakeRom('\x00'*0x480+'\x18\x03'))
		cpu.PC = 0x480
		cpu.readOp()
		self.assertEqual(12, cpu.t_states)

	def test_jp_hl_does_take_1_m_cycle(self):
		cpu = CPU(FakeRom('\xe9'))
		cpu.HL = 0x4800
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_jp_hl_does_take_4_t_states(self):
		cpu = CPU(FakeRom('\xe9'))
		cpu.HL = 0x4800
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_jp_ix_does_take_2_m_cycles(self):
		cpu = CPU(FakeRom('\xdd\xe9'))
		cpu.IX = 0x4600
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_jp_ix_does_take_8_t_states(self):
		cpu = CPU(FakeRom('\xdd\xe9'))
		cpu.IX = 0x4600
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)

	def test_jp_iy_does_take_2_m_cycles(self):
		cpu = CPU(FakeRom('\xfd\xe9'))
		cpu.IY = 0x4622
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_jp_iy_does_take_8_t_states(self):
		cpu = CPU(FakeRom('\xfd\xe9'))
		cpu.IY = 0x4622
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)
