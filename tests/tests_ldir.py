import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ldir(unittest.TestCase):

	def test_ldir(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x03
		cpu.ram[0x1111] = 0x88
		cpu.ram[0x1112] = 0x36
		cpu.ram[0x1113] = 0xA5
		cpu.ram[0x2222] = 0x66
		cpu.ram[0x2223] = 0x59
		cpu.ram[0x2224] = 0xc5
		cpu.readOp()
		self.assertEqual(0x1114, cpu.HL)
		self.assertEqual(0x2225, cpu.DE)
		self.assertEqual(0x0000, cpu.BC)

		self.assertEqual(0x88, cpu.ram[0x1111])
		self.assertEqual(0x36, cpu.ram[0x1112])
		self.assertEqual(0xa5, cpu.ram[0x1113])

		self.assertEqual(0x88, cpu.ram[0x2222])
		self.assertEqual(0x36, cpu.ram[0x2223])
		self.assertEqual(0xa5, cpu.ram[0x2224])

	def test_ldir_for_bc_not_equal_to_zero_takes_5_m_cycles(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x03
		cpu.ram[0x1111] = 0x88
		cpu.ram[0x1112] = 0x36
		cpu.ram[0x1113] = 0xA5
		cpu.ram[0x2222] = 0x66
		cpu.ram[0x2223] = 0x59
		cpu.ram[0x2224] = 0xc5
		cpu.readOp()
		self.assertEqual(5, cpu.m_cycles)

	def test_ldir_for_bc_equal_to_zero_takes_4_m_cycles(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x0
		cpu.ram[0x1111] = 0x88
		cpu.ram[0x1112] = 0x36
		cpu.ram[0x1113] = 0xA5
		cpu.ram[0x2222] = 0x66
		cpu.ram[0x2223] = 0x59
		cpu.ram[0x2224] = 0xc5
		cpu.readOp()
		self.assertEqual(4, cpu.m_cycles)

	def test_ldir_for_bc_not_equal_to_zero_takes_21_t_states(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x03
		cpu.ram[0x1111] = 0x88
		cpu.ram[0x1112] = 0x36
		cpu.ram[0x1113] = 0xA5
		cpu.ram[0x2222] = 0x66
		cpu.ram[0x2223] = 0x59
		cpu.ram[0x2224] = 0xc5
		cpu.readOp()
		self.assertEqual(21, cpu.t_states)

	def test_ldir_for_bc_equal_to_zero_takes_16_t_states(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x0
		cpu.ram[0x1111] = 0x88
		cpu.ram[0x1112] = 0x36
		cpu.ram[0x1113] = 0xA5
		cpu.ram[0x2222] = 0x66
		cpu.ram[0x2223] = 0x59
		cpu.ram[0x2224] = 0xc5
		cpu.readOp()
		self.assertEqual(16, cpu.t_states)
