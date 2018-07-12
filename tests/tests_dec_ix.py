import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_ix_sets_correct_value_is_set(self):
		ram = RAM()
		ram[0x105] = 0xDD
		cpu = CPU(FakeRom('\xdd\x35\x05'), ram)
		cpu.IX = 0x100
		cpu.readOp()
		self.assertEqual(0xDC, ram[cpu.IX+5])

	def test_dec_ix_takes_6_m_cycles(self):
		ram = RAM()
		ram[0x105] = 0xDD
		cpu = CPU(FakeRom('\xdd\x35\x05'), ram)
		cpu.IX = 0x100
		cpu.readOp()
		self.assertEqual(6, cpu.m_cycles)

	def test_dec_ix_takes_23_t_states(self):
		ram = RAM()
		ram[0x105] = 0xDD
		cpu = CPU(FakeRom('\xdd\x35\x05'), ram)
		cpu.IX = 0x100
		cpu.readOp()
		self.assertEqual(23, cpu.t_states)