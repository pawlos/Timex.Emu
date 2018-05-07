import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ex(unittest.TestCase):
	def test_ex_de_hl_exchanges_16_bit_hl_de_registers(self):
		cpu = CPU(FakeRom('\xeb'))
		cpu.HL = 0xabba
		cpu.DE = 0xc0de
		cpu.readOp()
		self.assertEqual(0xc0de, cpu.HL)
		self.assertEqual(0xabba, cpu.DE)

	def test_ex_de_hl_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\xeb'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_ex_de_hl_takes_4_t_states(self):
		cpu = CPU(FakeRom('\xeb'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)