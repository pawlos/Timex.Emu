import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_pop(unittest.TestCase):

	def test_pop_ix_correctly_retreives_value_from_stack(self):
		ram = RAM()
		ram[0x1000] = 0x55
		ram[0x1001] = 0x33
		cpu = CPU(FakeRom('\xdd\xe1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.IX)

	def test_pop_ix_takes_4_m_cycles(self):
		ram = RAM()
		ram[0x1000] = 0x55
		ram[0x1001] = 0x33
		cpu = CPU(FakeRom('\xdd\xe1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(4, cpu.m_cycles)

	def test_pop_ix_takes_14_t_states(self):
		ram = RAM()
		ram[0x1000] = 0x55
		ram[0x1001] = 0x33
		cpu = CPU(FakeRom('\xdd\xe1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(14, cpu.t_states)