import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_sub(unittest.TestCase):

	def test_sub_n_set_corrects_value(self):
		cpu = CPU(ROM('\xd6\x52'))
		cpu.A = 0x52
		cpu.readOp()
		self.assertEqual(0x00, cpu.A)

	def test_sub_n_set_ZFlag_if_value_is_zero(self):
		cpu = CPU(ROM('\xd6\x52'))
		cpu.A = 0x52
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_sub_r_set_correct_value(self):
		cpu = CPU(ROM('\x90'))
		cpu.A = 0x52
		cpu.B = 0x02
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_r_takes_1_m_cycles(self):
		cpu = CPU(ROM('\x90'))
		cpu.A = 0x52
		cpu.B = 0x02
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_sub_r_takes_4_t_states(self):
		cpu = CPU(ROM('\x90'))
		cpu.A = 0x52
		cpu.B = 0x02
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

