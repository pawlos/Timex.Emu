import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_in(unittest.TestCase):

	def test_in_from_port_specified_in_c_puts_value_of_reg_A(self):
		cpu = CPU(ROM('\xed\x78'))
		cpu.C = 0x44
		cpu.io.writeTo(cpu.C, 0xAA)
		
		cpu.readOp()
		self.assertEqual(0xAA, cpu.io.readFrom(0x44))

	def test_in_from_port_takes_3_m_cycles(self):
		cpu = CPU(ROM('\xed\x78'))
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_in_from_port_takes_12_t_states(self):
		cpu = CPU(ROM('\xed\x78'))
		cpu.readOp()
		self.assertEqual(12, cpu.t_states)