import unittest
from cpu import CPU
from fakes import *

class tests_timings(unittest.TestCase):

	def test_2_nops_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\x00\x00'))
		cpu.readOp()
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_2_nop_takes_8_t_states(self):
		cpu = CPU(FakeRom('\x00\x00'))
		cpu.readOp()
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)

	def test_nop_takes_1_m_cycles(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_nop_takes_4_t_states(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_ld16_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\x01'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ld16_takes_10_t_states(self):
		cpu = CPU(FakeRom('\x01'))
		cpu.readOp()
		self.assertEqual(10, cpu.t_states)

	def test_ld_bc_a_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\x02'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ld_bc_a_takes_7_t_states(self):
		cpu = CPU(FakeRom('\x02'))
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_inc_bc_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\x03'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_inc_bc_takes_6_t_states(self):
		cpu = CPU(FakeRom('\x03'))
		cpu.readOp()
		self.assertEqual(6, cpu.t_states)

	def test_inc_b_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_inc_b_takes_4_t_states(self):
		cpu = CPU(FakeRom('\x04'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_dec_b_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\x05'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_dec_b_takes_4_t_states(self):
		cpu = CPU(FakeRom('\x05'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_ld_r_n_takes_2_m_cycle(self):
		cpu = CPU(FakeRom('\x06'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ld_r_n_takes_7_t_states(self):
		cpu = CPU(FakeRom('\x06'))
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_ei_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\xfb'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_ei_takes_4_t_states(self):
		cpu = CPU(FakeRom('\xfb'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_di_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\xf3'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_di_takes_4_m_cycles(self):
		cpu = CPU(FakeRom('\xf3'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_xor_a_takes_1_m_cycles(self):
		cpu = CPU(FakeRom('\xa8'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_xor_a_takes_4_t_states(self):
		cpu = CPU(FakeRom('\xa8'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_add_hl_takes_3_m_cycles(self):
		cpu = CPU(FakeRom('\x09'))
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_add_hl_takes_11_t_states(self):
		cpu = CPU(FakeRom('\x09'))
		cpu.readOp()
		self.assertEqual(11, cpu.t_states)

	def test_rrca_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\x0f'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_rrca_takes_4_t_states(self):
		cpu = CPU(FakeRom('\x0f'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)