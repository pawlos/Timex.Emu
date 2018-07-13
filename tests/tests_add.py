import unittest
from cpu import CPU
from rom import ROM
from opcodes import Opcodes
from loggers import Logger

class tests_add(unittest.TestCase):

	def test_add_hl_de_returns_correct_result(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0xabba, cpu.HL)

	def test_add_hl_bc_returns_correct_result(self):
		cpu = CPU(ROM('\x09'))
		cpu.HL = 0xa00a
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(0xabba, cpu.HL)

	def test_add_hl_sp_returns_correct_result(self):
		cpu = CPU(ROM('\x39'))
		cpu.HL = 0xa00a
		cpu.SP = 0x0bb0
		cpu.readOp()
		self.assertEqual(0xabba, cpu.HL)

	def test_add_hl_hl_returns_correct_result(self):
		cpu = CPU(ROM('\x29'))
		cpu.HL = 0x300a
		cpu.readOp()
		self.assertEqual(0x6014, cpu.HL)

	def test_add_hl_de_limits_the_result_to_16bits(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xf000
		cpu.DE = 0x1000
		cpu.readOp()
		self.assertEqual(0x0, cpu.HL)

	def test_add_hl_de_does_not_change_s_flag(self):
		cpu = CPU(ROM('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.SFlag = False
		cpu.readOp()
		self.assertFalse(cpu.SFlag)
		cpu.SFlag = True
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_add_hl_de_does_not_change_z_flag(self):
		cpu = CPU(ROM('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.ZFlag = True
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)
		cpu.ZFlag = False
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_add_hl_de_does_not_change_pv_flag(self):
		cpu = CPU(ROM('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.PVFlag = False
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)
		cpu.PVFlag = True
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_add_hl_de_resets_n_flag(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xb0b0
		cpu.DE = 0x0a0a
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_add_hl_de_sets_c_if_carry_from_bit_15(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xf000
		cpu.DE = 0x1000
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_hl_de_resets_c_flag_if_carry_does_not_occur(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xf000
		cpu.DE = 0x0fff
		cpu.CFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_add_hl_de_sets_h_flag_if_carry_from_bit_11(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0x0f00
		cpu.DE = 0x0100
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_add_hl_de_resets_h_flag_if_carry_from_bit_11_does_not_occur(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0x0f00
		cpu.DE = 0x00ff
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_add_hl_de_does_not_exceed_limit_of_16_bits(self):
		cpu = CPU(ROM('\x19'))
		cpu.HL = 0xaaaa
		cpu.DE = 0xaaaa
		cpu.readOp()
		self.assertEqual(0x5554, cpu.HL)

	def test_add_A_n_correctly_calculates_value(self):
		cpu = CPU(ROM('\xC6\x33'))
		cpu.A = 0x23
		cpu.readOp()
		self.assertEqual(0x56, cpu.A)

	def test_add_A_n_correctly_set_Z_flag_when_value_is_0(self):
		cpu = CPU(ROM('\xC6\x33'))
		cpu.A = 0x0-0x33
		cpu.ZFlag = False
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_add_A_n_correctly_set_C_flag_when_value_is_outside_range(self):
		cpu = CPU(ROM('\xC6\x33'))
		cpu.A = 0xCD
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_A_n_correctly_set_S_flag_when_value_is_outside_negative(self):
		cpu = CPU(ROM('\xC6\x03'))
		cpu.A = 0xCD
		cpu.SFlag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_add_A_A_correctly_calculates_value(self):
		cpu = CPU(ROM('\x87'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(0x24, cpu.A)

	def test_add_A_E_correctly_calculates_value(self):
		cpu = CPU(ROM('\x83'))
		cpu.A = 0x12
		cpu.E = 0x10
		cpu.readOp()
		self.assertEqual(0x22, cpu.A)

	def test_add_A_L_correctly_calculates_value(self):
		cpu = CPU(ROM('\x85'))
		cpu.A = 0x12
		cpu.L = 0xE0
		cpu.readOp()
		self.assertEqual(0xF2, cpu.A)
	
	def test_add_A_C_correctly_calculates_value(self):
		cpu = CPU(ROM('\x81'))
		cpu.A = 0x12
		cpu.C = 0x30
		cpu.readOp()
		self.assertEqual(0x42, cpu.A)

	def test_add_A_B_correctly_calculates_value(self):
		cpu = CPU(ROM('\x80'))
		cpu.A = 0x12
		cpu.B = 0x40
		cpu.readOp()
		self.assertEqual(0x52, cpu.A)

	def test_add_A_H_correctly_calculates_value(self):
		cpu = CPU(ROM('\x84'))
		cpu.A = 0x12
		cpu.H = 0x60
		cpu.readOp()
		self.assertEqual(0x72, cpu.A)

	def test_add_A_D_correctly_calculates_value(self):
		cpu = CPU(ROM('\x82'))
		cpu.A = 0x12
		cpu.D = 0x90
		cpu.readOp()
		self.assertEqual(0xA2, cpu.A)

	def test_add_a_hl_correctly_adds_value_from_address(self):
		cpu = CPU(ROM('\x86'))
		cpu.HL = 0x0
		cpu.A = 0x14
		cpu.readOp()
		self.assertEqual(0x9a, cpu.A)

	def test_add_a_hl_correctly_sets_z_flag_if_result_is_zero(self):
		cpu = CPU(ROM('\x86\xA0'))
		cpu.HL = 0x1
		cpu.A = 0x60
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_add_a_hl_correctly_sets_s_flag_if_result_is_negative(self):
		cpu = CPU(ROM('\x86\xA0'))
		cpu.HL = 0x1
		cpu.A = 0x50
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_add_a_hl_correctly_sets_c_flag_if_result_is_overflow(self):
		cpu = CPU(ROM('\x86\xA0'))
		cpu.HL = 0x1
		cpu.A = 0x61
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_a_hl_takes_2_m_cycles(self):
		cpu = CPU(ROM('\x86\xA0'))
		cpu.HL = 0x1
		cpu.A = 0x61
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_add_a_hl_takes_7_t_states(self):
		cpu = CPU(ROM('\x86\xA0'))
		cpu.HL = 0x1
		cpu.A = 0x61
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)

	def test_add_hl_takes_3_m_cycles(self):
		cpu = CPU(ROM('\x09'))
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_add_hl_takes_11_t_states(self):
		cpu = CPU(ROM('\x09'))
		cpu.readOp()
		self.assertEqual(11, cpu.t_states)

	def test_add_A_B_takes_1_m_cycle(self):
		cpu = CPU(ROM('\x80'))
		cpu.A = 0x12
		cpu.B = 0x40
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_add_A_B_takes_4_t_states(self):
		cpu = CPU(ROM('\x80'))
		cpu.A = 0x12
		cpu.B = 0x40
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

	def test_add_A_n_takes_2_m_cycles(self):
		cpu = CPU(ROM('\xc6\x22'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_add_A_n_takes_7_t_states(self):
		cpu = CPU(ROM('\xc6\x22'))
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)