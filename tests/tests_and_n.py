import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_and_n(unittest.TestCase):
	def test_and_n_performs_and_operation(self):
		cpu = CPU(FakeRom('\xe6\x10'))
		cpu.A = 0x01
		cpu.readOp()
		self.assertEqual(0x0, cpu.A)

	def test_and_n_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\xe6\x10'))
		cpu.A = 0x01
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)	
		
	def test_and_n_takes_7_t_states(self):
		cpu = CPU(FakeRom('\xe6\x10'))
		cpu.A = 0x01
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)	
