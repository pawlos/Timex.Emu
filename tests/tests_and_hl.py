import unittest

from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_and_hl(unittest.TestCase):
	def test_and_hl_performs_and_operation(self):
		cpu = CPU(ROM('\xa6\x00\x10'))
		cpu.A = 0x01
		cpu.HL = 0x02
		cpu.readOp()
		self.assertEqual(0x0, cpu.A)

	def test_and_hl_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xa6\x00\x10'))
		cpu.A = 0x01
		cpu.HL = 0x02
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)	
		
	def test_and_hl_takes_7_t_states(self):
		cpu = CPU(ROM('\xa6\x00\x10'))
		cpu.A = 0x01
		cpu.HL = 0x02
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)	
