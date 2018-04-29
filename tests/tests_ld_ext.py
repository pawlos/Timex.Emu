from  cpu import *
from fakes import *
import unittest


class tests_ld_ext(unittest.TestCase):

	def test_ld_I_A_correctly_assigns_value(self):
		cpu = CPU(FakeRom('\xed\x47'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(0x33, cpu.I)

	def test_ld_I_A_takes_3_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x47'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_ld_I_A_takes_9_t_states(self):
		cpu = CPU(FakeRom('\xed\x47'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(9, cpu.t_states)