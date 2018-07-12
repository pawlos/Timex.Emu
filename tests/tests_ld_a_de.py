import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_a_de(unittest.TestCase):

	def test_ld_a_de_loads_corect_value(self):
		ram = RAM()
		ram[0x30A2] = 0x22
		cpu = CPU(FakeRom('\x1a'), ram)
		cpu.DE = 0x30A2
		cpu.readOp()
		self.assertEqual(0x22, cpu.A)

	def test_ld_a_de_takes_2_m_cycles(self):
		ram = RAM()
		ram[0x30A2] = 0x22
		cpu = CPU(FakeRom('\x1a'), ram)
		cpu.DE = 0x30A2
		cpu.readOp()
		self.assertEqual(2,cpu.m_cycles)

	def test_ld_a_de_takes_7_t_states(self):
		ram = RAM()
		ram[0x30A2] = 0x22
		cpu = CPU(FakeRom('\x1a'), ram)
		cpu.DE = 0x30A2
		cpu.readOp()
		self.assertEqual(7,cpu.t_states)