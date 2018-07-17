import unittest

from cpu import CPU

class tests_cp_n(unittest.TestCase):

	def test_cp_n_takes_2_m_cycles(self):
		cpu = CPU('\xfe\x02')
		cpu.readOp()
		self.assertEquals(2, cpu.m_cycles)

	def test_cp_n_takes_7_t_states(self):
		cpu = CPU('\xfe\x02')
		cpu.readOp()
		self.assertEquals(7, cpu.t_states)

	def test_cp_n_correctly_sets_ZFlag_when_value_is_zero(self):
		cpu = CPU('\xfe\x02')
		cpu.A = 0x2
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_n_correctly_sets_SFlag_to_true_when_value_is_negative(self):
		cpu = CPU('\xfe\x05')
		cpu.A = 0x2
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_n_correctly_sets_SFlag_to_false_when_value_is_positive(self):
		cpu = CPU('\xfe\x05')
		cpu.A = 0x5
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_cp_n_correctly_sets_HFlag_to_true_when_borrow_on_bit_4(self):
		cpu = CPU('\xfe\x0f')
		cpu.A = 0x10
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_cp_n_correctly_sets_PVFlag_to_true_when_overflow(self):
		cpu = CPU('\xfe\x01')
		cpu.A = 0x81
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_cp_n_correctly_sets_NFlag_always_to_true(self):
		cpu = CPU('\xfe\xff')
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_cp_n_correctly_Sets_CFlag_when_borrow(self):
		cpu = CPU('\xfe\x01')
		cpu.A = 0x00
		cpu.readOp()
		self.assertTrue(cpu.CFlag)