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

	def test_sub_B_set_correct_value(self):
		cpu = CPU(ROM('\x90'))
		cpu.A = 0x52
		cpu.B = 0x02
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_C_set_correct_value(self):
		cpu = CPU(ROM('\x91'))
		cpu.A = 0x53
		cpu.C = 0x03
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_D_set_correct_value(self):
		cpu = CPU(ROM('\x92'))
		cpu.A = 0x54
		cpu.D = 0x04
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_E_set_correct_value(self):
		cpu = CPU(ROM('\x93'))
		cpu.A = 0x55
		cpu.E = 0x05
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_H_set_correct_value(self):
		cpu = CPU(ROM('\x94'))
		cpu.A = 0x53
		cpu.H = 0x03
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_L_set_correct_value(self):
		cpu = CPU(ROM('\x95'))
		cpu.A = 0x53
		cpu.L = 0x03
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_sub_A_set_correct_value(self):
		cpu = CPU(ROM('\x97'))
		cpu.A = 0x53
		cpu.readOp()
		self.assertEqual(0, cpu.A)		

	def test_sub_A_B_takes_1_m_cycles(self):
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

	def test_sub_a_hl_correctly_calculates_value(self):
		cpu = CPU(ROM('\x96\x00\x00\x22'))
		cpu.A = 0x52
		cpu.HL = 0x3
		cpu.readOp()
		self.assertEqual(0x30, cpu.A)

	def test_sub_r_takes_1_m_cycles(self):
		cpu = CPU(ROM('\x96\x00\x00\x22'))
		cpu.A = 0x52
		cpu.HL = 0x3
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_sub_r_takes_7_t_states(self):
		cpu = CPU(ROM('\x96\x00\x00\x22'))
		cpu.A = 0x52
		cpu.HL = 0x3
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)
