import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_lra(unittest.TestCase):

	def test_lra_does_modify_value_correctly(self):
		cpu = CPU(ROM('\x17'))
		cpu.A = 0b01110110
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0b11101101, cpu.A)
		self.assertFalse(cpu.CFlag)

	def test_lra_does_take_1_m_cycles(self):
		cpu = CPU(ROM('\x17'))
		cpu.A = 0b01110110
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_lra_does_take_4_t_states(self):
		cpu = CPU(ROM('\x17'))
		cpu.A = 0b01110110
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)