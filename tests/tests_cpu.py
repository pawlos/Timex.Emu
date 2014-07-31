import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger


class TestCPUFunctions(unittest.TestCase):
	def test_init_zeros_registers(self):
		cpu = CPU(FakeRom('\x00'))
		self.assertEqual(0, cpu.A)
		self.assertEqual(0, cpu.B)
		self.assertEqual(0, cpu.C)
		self.assertEqual(0, cpu.D)
		self.assertEqual(0, cpu.E)
		self.assertEqual(0, cpu.H)
		self.assertEqual(0, cpu.L)

	def test_xor_A_works_correctly(self):
		cpu = CPU(FakeRom('\xb0'))
		cpu.A = 12
		cpu.B = 11
		cpu.readOp()
		self.assertEqual(7, cpu.A)

	def test_if_A_is_set_to_96H_xor_5DH_works(self):
		cpu = CPU(FakeRom('\xb0'))
		cpu.A = 0x96
		cpu.B = 0x5D
		cpu.readOp()
		self.assertEqual(0xCB, cpu.A)

	def test_if_A_xors_to_zero_Z_is_set(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.readOp()
		self.assertEqual(0, cpu.A)
		self.assertEqual(True, cpu.ZFlag)

	def test_if_A_xors_to_non_zero_Z_is_reset(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.ZFlag = True
		cpu.readOp()
		self.assertNotEqual(0, cpu.A)
		self.assertFalse(cpu.ZFlag)

	def test_xor_A_resets_C_flag(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.CFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_xor_A_resets_N_flag(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_xor_A_resets_H_flag(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_xor_A_sets_S_if_result_is_negative(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x96
		cpu.C = 0x5D
		cpu.SFlag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_xor_A_resets_S_if_result_is_positive(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x12
		cpu.C = 0x55
		cpu.SFlag = True
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_xor_A_sets_PV_if_parity_even(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x44
		cpu.C = 0x11
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_xor_A_resets_PV_if_parity_odd(self):
		cpu = CPU(FakeRom('\xb1'))
		cpu.A = 0x45
		cpu.C = 0x11
		cpu.PVFlag = True
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)

	def test_HL_property_assign_correct_values_to_H_and_L(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.HL = 0x1123
		self.assertEqual(0x11, cpu.H)
		self.assertEqual(0x23, cpu.L)

	def test_HL_property_has_correct_value_when_H_and_L_are_set(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.H = 0x66
		cpu.L = 0x01
		self.assertEqual(0x6601, cpu.HL)

	def test_JP_XX_sets_PC_correctly(self):
		cpu = CPU(FakeRom('\xc3\xcb\x11'))
		cpu.PC = 0
		cpu.readOp()
		self.assertEqual(0x11cb, cpu.PC)

	def test_ld_B_A_works_correctly(self):
		cpu = CPU(FakeRom('\x47'))
		cpu.A = 0x5D
		cpu.B = 0x11
		cpu.readOp()
		self.assertEqual(0x5d, cpu.B)
		self.assertEqual(0x5d, cpu.A)

	def test_ld_A_07_works_correctly(self):
		cpu = CPU(FakeRom('\x3e\x07'))
		cpu.readOp()
		self.assertEqual(0x07, cpu.A)

	def test_double_byte_opcode_results_in_correct_assigment(self):
		cpu = CPU(FakeRom('\xed\x47'))
		cpu.A = 0x33
		cpu.readOp()
		self.assertEqual(0x33, cpu.I)

	def test_registers_are_accessible_by_index_and_name(self):
		cpu = CPU(None)
		cpu.regs[0] = 0x11
		self.assertEqual(0x11, cpu.B)

	def test_0x62_opcode_correctly_maps_to_LD_H_D(self):
		cpu = CPU(FakeRom('\x62'))
		cpu.D = 0xaa
		cpu.readOp()
		self.assertEqual(0xaa, cpu.H)

	def test_0x6b_opcode_correctly_maps_to_LD_L_E(self):
		cpu = CPU(FakeRom('\x6b'))
		cpu.E = 0xbb
		cpu.readOp()
		self.assertEqual(0xbb, cpu.L)

	def test_0x36nn_opcodes_does_set_value_in_address_pointed_by_HL(self):
		ram = FakeRam()
		cpu = CPU(FakeRom('\x36\x22'), ram)	
		cpu.HL = 0x2222
		cpu.readOp()
		self.assertEqual(0x22, ram.readAddr(0x2222))

	def test_0x2b_opcode_does_decrement_HL(self):
		cpu = CPU(FakeRom('\x2b'))
		cpu.HL = 0x1101
		cpu.readOp();
		self.assertEqual(0x1100, cpu.HL)

	def test_16bit_registers_are_accessed_by_8bit_parts(self):
		cpu = CPU(None)
		cpu.HL = 0x1234

		self.assertEqual(0x12, cpu.H)
		self.assertEqual(0x34, cpu.L)

	def test_16bit_registers(self):
		cpu = CPU(FakeRom('\x2b'))
		cpu.HL = 0x0100
		cpu.readOp()
		self.assertEqual(0x00, cpu.H)
		self.assertEqual(0xFF, cpu.L)

	def test_cp_H_sets_ZF_if_H_is_equal_to_0(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 3
		cpu.H = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_H_resets_ZF_if_H_is_not_equal_to_0(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 1
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_cp_H_sets_SF_if_H_is_negative(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 1
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_H_sets_NF_always(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 0
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_cp_H_sets_CF_is_results_goes_below_zero(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 3
		cpu.H = 0xff
		cpu.readOp();
		self.assertTrue(cpu.CFlag)

	def test_cp_H_sets_HF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x10
		cpu.H = 0x01
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_cp_H_resets_HF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x3
		cpu.H = 0x1
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_cp_H_sets_PVF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x7f
		cpu.H = 0x81
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_jp_nz_jumps_if_ZFlag_is_non_zero(self):
		rom = [None] * 0x0482
		rom[0x480] = '\x20'
		rom[0x481] = '\xFA'
		cpu = CPU(FakeRom(rom))
		cpu.PC = 0x0480
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x047C, cpu.PC)

	def test_jp_nz_does_not_jump_if_ZFlag_is_set(self):
		cpu = CPU(FakeRom('\x20\xFA'))
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x02, cpu.PC)

	def test_and_a_performs_and_operation(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.A = 0x12
		cpu.readOp()
		self.assertEqual(0x12, cpu.A)

	def test_and_a_sets_HFlag(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.A = 0x12
		cpu.HFlag = False
		cpu.readOp();
		self.assertTrue(cpu.HFlag)

	def test_and_a_resets_n_and_c_flag(self):
		cpu = CPU(FakeRom('\xa7'))
		cpu.CFlag = True
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)
		self.assertFalse(cpu.NFlag)

	def test_and_h_that_returns_0_set_z_flag(self):
		cpu = CPU(FakeRom('\xa4'))
		cpu.H = 0x10
		cpu.A = 0x01
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_and_h_that_returns_non_0_reset_z_flag(self):
		cpu = CPU(FakeRom('\xa4'))
		cpu.H = 0x11
		cpu.A = 0x10
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_and_h_that_returns_negative_set_s_flag(self):
		cpu = CPU(FakeRom('\xa4'))
		cpu.H = 0x88
		cpu.A = 0x81
		cpu.SFlag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_and_h_that_returns_positive_resets_s_flag(self):
		cpu = CPU(FakeRom('\xa4'))
		cpu.H = 0x88
		cpu.A = 0x08
		cpu.SFlag = True
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

if __name__ == '__main__':
	unittest.main()