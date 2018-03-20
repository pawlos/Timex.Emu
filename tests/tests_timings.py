import unittest
from cpu import CPU
from fakes import *

class tests_timings(unittest.TestCase):

	def test_nop_takes_1_m_cycles(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_nop_takes_1_t_states(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_ld16_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\x01'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ld16_takes_2_t_states(self):
		cpu = CPU(FakeRom('\x01'))
		cpu.readOp()
		self.assertEqual(10, cpu.t_states)
