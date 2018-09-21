import unittest

from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_or_a(unittest.TestCase):
	def test_or_a_performs_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xf6\x48'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(0x5A, cpu.A)

	def test_or_a_performs_or_operation_Z_is_set_when_value_is_zero(self):
		cpu = CPU(ROM('\xf6\x00'))
		cpu.ZFlag = False
		cpu.A = 0x00
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_or_a_performs_or_operation_S_is_set_when_value_is_negative(self):
		cpu = CPU(ROM('\xf6\x00'))
		cpu.SFlag = False
		cpu.A = 0xCD
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_or_a_e_perform_or_operation_and_ZFlag_is_set_when_result_is_0(self):
		cpu = CPU(ROM('\xb3'))
		cpu.A = 0x00
		cpu.E = 0x00
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_or_a_b_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb0'))
		cpu.A = 0x01
		cpu.B = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)

	def test_or_a_c_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb1'))
		cpu.A = 0x01
		cpu.C = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)

	def test_or_a_d_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb2'))
		cpu.A = 0x01
		cpu.D = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)

	def test_or_a_e_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb3'))
		cpu.A = 0x01
		cpu.E = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)

	def test_or_a_h_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb4'))
		cpu.A = 0x01
		cpu.H = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)


	def test_or_a_l_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb5'))
		cpu.A = 0x01
		cpu.L = 0x04
		cpu.readOp()
		self.assertEqual(0x05, cpu.A)


	def test_or_a_a_perform_or_operation_value_is_correct(self):
		cpu = CPU(ROM('\xb7'))
		cpu.A = 0x00
		cpu.B = 0x01
		cpu.C = 0x02
		cpu.D = 0x04
		cpu.E = 0x08
		cpu.H = 0x0a
		cpu.L = 0x10
		cpu.readOp()
		self.assertEqual(0x00, cpu.A)

	def test_or_n_takes_2_m_cycles(self):
		cpu = CPU(ROM('\xf6\x48'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_or_n_takes_7_t_states(self):
		cpu = CPU(ROM('\xf6\x48'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_or_a_b_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xb0'))
		cpu.A = 0x01
		cpu.B = 0x04
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_or_a_b_takes_4_t_states(self):
		cpu = CPU(ROM('\xb0'))
		cpu.A = 0x01
		cpu.B = 0x04
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_or_hl_correctly_perform_operation(self):
		cpu = CPU(ROM('\xb6\x05\x06\x00\x09'))
		cpu.HL = 0x04
		cpu.A = 0x02
		cpu.readOp()
		self.assertEqual(0b1011, cpu.A)

	def test_or_hl_correctly_sets_ZFlag(self):
		cpu = CPU(ROM('\xb6\x05\x06\x00\x00'))
		cpu.HL = 0x04
		cpu.A = 0x00
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_or_hl_takes_2_m_cycles(self):
		cpu = CPU(ROM('\xb6\x05\x06\x00\x00'))
		cpu.HL = 0x04
		cpu.A = 0x00
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_or_hl_takes_7_t_states(self):
		cpu = CPU(ROM('\xb6\x05\x06\x00\x00'))
		cpu.HL = 0x04
		cpu.A = 0x00
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)
