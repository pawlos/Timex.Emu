import unittest

from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_iy_r(unittest.TestCase):
	
	def test_ld_iy_d_l_correctly_copies_value_to_memory(self):
		ram = RAM()
		cpu = CPU(FakeRom('\xFD\x75\x10'), ram)
		cpu.IY = 0x25AF
		cpu.L = 0x39
		cpu.readOp()
		self.assertEqual(0x39, ram[0x25bf])

	def test_ld_iy_d_l_takes_5_m_cycles(self):
		ram = RAM()
		cpu = CPU(FakeRom('\xFD\x75\x10'), ram)
		cpu.IY = 0x25AF
		cpu.L = 0x39
		cpu.readOp()
		self.assertEqual(5, cpu.m_cycles)

	def test_ld_iy_d_l_takes_19_t_states(self):
		ram = RAM()
		cpu = CPU(FakeRom('\xFD\x75\x10'), ram)
		cpu.IY = 0x25AF
		cpu.L = 0x39
		cpu.readOp()
		self.assertEqual(19, cpu.t_states)		
