import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_dec(unittest.TestCase):

	def test_dec_b_sets_correct_value_is_set(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x01
		cpu.readOp()
		self.assertEqual(0x00, cpu.B)

	def test_dec_b_sets_z_flag_if_value_is_zero(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x01
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_dec_b_resets_z_flag_if_value_is_non_zero(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x00
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_dec_b_sets_s_flag_if_value_is_negative(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x00
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_dec_b_resets_s_flag_if_value_is_positive(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x02
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_dec_b_sets_n_flag(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x02
		cpu.NFlag = False
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_dec_b_sets_PV_flag_if_borrow(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0b00010000
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_dec_b_sets_h_flag_if_borrow_from_bit_4(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0b00010000
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_dec_b_resets_h_flag_if_no_borrow_from_bit_4(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0b00011000
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_dec_b_sets_pv_flag_if_value_was_80h(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x80
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_dec_b_resets_pv_flag_if_value_was_not_80h(self):
		cpu = CPU(FakeRom('\x05'), FakeRam())
		cpu.B = 0x7f
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)

	def test_dec_c_sets_correct_value(self):
		cpu = CPU(FakeRom('\x0D'), FakeRam())
		cpu.C = 10
		cpu.readOp()
		self.assertEqual(9, cpu.C)

	def test_dec_d_sets_correct_value(self):
		cpu = CPU(FakeRom('\x15'), FakeRam())
		cpu.D = 0xFF
		cpu.readOp()
		self.assertEqual(0xFE, cpu.D)

	def test_dec_e_sets_correct_value(self):
		cpu = CPU(FakeRom('\x1d'),FakeRam())
		cpu.E = 0x15
		cpu.readOp()
		self.assertEqual(0x14, cpu.E)

	def test_dec_H_sets_correct_value(self):
		cpu = CPU(FakeRom('\x25'),FakeRam())
		cpu.H = 0x25
		cpu.readOp()
		self.assertEqual(0x24, cpu.H)

	def test_dec_L_sets_correct_value(self):
		cpu = CPU(FakeRom('\x2D'),FakeRam())
		cpu.L = 0x50
		cpu.readOp()
		self.assertEqual(0x4f, cpu.L)

	def test_dec_A_sets_correct_value(self):
		cpu = CPU(FakeRom('\x3D'),FakeRam())
		cpu.A = 0x51
		cpu.readOp()
		self.assertEqual(0x50, cpu.A)

	def test_dec_b_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\x05'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_dec_b_takes_4_t_states(self):
		cpu = CPU(FakeRom('\x05'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_dec_bc_opcode_does_decrement_BC(self):
		cpu = CPU(FakeRom('\x0B'))
		cpu.BC = 0x1101
		cpu.readOp()
		self.assertEqual(0x1100, cpu.BC)

	def test_dec_de_opcode_does_decrement_DE(self):
		cpu = CPU(FakeRom('\x1B'))
		cpu.DE = 0x1101
		cpu.readOp()
		self.assertEqual(0x1100, cpu.DE)

	def test_dec_hl_opcode_does_decrement_HL(self):
		cpu = CPU(FakeRom('\x2B'))
		cpu.HL = 0x1101
		cpu.readOp()
		self.assertEqual(0x1100, cpu.HL)

	def test_dec_sp_opcode_does_decrement_SP(self):
		cpu = CPU(FakeRom('\x3b'))
		cpu.SP = 0x1101
		cpu.readOp()
		self.assertEqual(0x1100, cpu.SP)

	def test_dec_bc_takes_1_m_cycles(self):
		cpu = CPU(FakeRom('\x0B'))
		cpu.BC = 0x1101
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_dec_bc_takes_6_t_states(self):
		cpu = CPU(FakeRom('\x0B'))
		cpu.BC = 0x1101
		cpu.readOp()
		self.assertEqual(6, cpu.t_states)