import unittest

from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_ix_nn(unittest.TestCase):
	''' DD 2A n n '''
	def test_ld_ix_nn_correctly_copies_nn_value_to_ix(self):
		ram = RAM()
		ram[0x6666] = 0x92
		ram[0x6667] = 0xDA
		cpu = CPU(FakeRom('\xDD\x2A\x66\x66'), ram)
		cpu.readOp()
		self.assertEqual(0xDA92, cpu.IX)

	def test_ld_ix_nn_takes_6_m_cycles(self):
		ram = RAM()
		ram[0x6666] = 0x92
		ram[0x6667] = 0xDA
		cpu = CPU(FakeRom('\xDD\x2A\x66\x66'), ram)
		cpu.readOp()
		self.assertEqual(6, cpu.m_cycles)

	def test_ld_ix_nn_takes_20_t_states(self):
		ram = RAM()
		ram[0x6666] = 0x92
		ram[0x6667] = 0xDA
		cpu = CPU(FakeRom('\xDD\x2A\x66\x66'), ram)
		cpu.readOp()
		self.assertEqual(20, cpu.t_states)
