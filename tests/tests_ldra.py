import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_ldra(unittest.TestCase):

	def test_ldra_does_copy_value_correctly_from_A_to_R(self):
		cpu = CPU(ROM('\xed\x4f'))
		cpu.A = 0b01110110
		cpu.readOp()
		self.assertEqual(0b01110110, cpu.R)

	def test_ldra_takes_2_m_cycles(self):
		cpu = CPU(ROM('\xed\x4f'))
		cpu.A = 0b01110110
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ldra_takes_9_t_states(self):
		cpu = CPU(ROM('\xed\x4f'))
		cpu.A = 0b01110110
		cpu.readOp()
		self.assertEqual(9, cpu.t_states)