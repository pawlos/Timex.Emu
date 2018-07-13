import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_out(unittest.TestCase):

	def test_out_to_port_0x22_puts_value_of_reg_A_to_port_0x22(self):
		cpu = CPU(ROM('\xd3\x22'))
		cpu.A = 0x33
		
		cpu.readOp()
		self.assertEqual(0x33, cpu.io.readFrom(0x22))

	def test_out_to_port_0x22_takes_3_m_cycles(self):
		cpu = CPU(ROM('\xd3\x22'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_out_to_port_0x22_takes_11_t_states(self):
		cpu = CPU(ROM('\xd3\x22'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(11, cpu.t_states)