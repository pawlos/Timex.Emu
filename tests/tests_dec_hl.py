import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_hl_sets_correct_value_is_set(self):
		ram = RAM()
		ram[0x100] = 0xDD
		cpu = CPU(FakeRom('\x35'), ram)
		cpu.HL = 0x100
		cpu.readOp()
		self.assertEqual(0xDC, ram[cpu.HL])

	def test_dec_hl_takes_3_m_cycles(self):
		ram = RAM()
		ram[0x100] = 0xDD
		cpu = CPU(FakeRom('\x35'), ram)
		cpu.HL = 0x100
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_dec_hl_takes_11_t_states(self):
		ram = RAM()
		ram[0x100] = 0xDD
		cpu = CPU(FakeRom('\x35'), ram)
		cpu.HL = 0x100
		cpu.readOp()
		self.assertEqual(11, cpu.t_states)
