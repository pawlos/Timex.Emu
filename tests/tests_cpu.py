import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from opcodes import Opcodes
from fake_rom import FakeRom


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
		cpu.pc = 0
		cpu.readOp()
		self.assertEqual(0x11cb, cpu.pc)

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

if __name__ == '__main__':
	unittest.main()