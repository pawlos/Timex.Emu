import unittest
from cpu import CPU
from fake_rom import FakeRom


class TestCPUFunctions(unittest.TestCase):
	def test_init_zeros_registers(self):
		cpu = CPU(None)
		self.assertEqual(0, cpu.A)
		self.assertEqual(0, cpu.B)
		self.assertEqual(0, cpu.C)
		self.assertEqual(0, cpu.D)
		self.assertEqual(0, cpu.E)
		self.assertEqual(0, cpu.H)
		self.assertEqual(0, cpu.L)

	def test_xor_A_works_correctly(self):
		cpu = CPU(None)
		cpu.A = 12
		cpu.B = 11
		cpu.xorA(0)
		self.assertEqual(7, cpu.A)

	def test_if_A_is_set_to_96H_xor_5DH_works(self):
		cpu = CPU(None)
		cpu.A = 0x96
		cpu.B = 0x5D
		cpu.xorA(0)
		self.assertEqual(0xCB, cpu.A)

	def test_if_A_xors_to_zero_Z_is_set(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.xorA(1)
		self.assertEqual(0, cpu.A)
		self.assertEqual(True, cpu.ZFlag)

	def test_if_A_xors_to_non_zero_Z_is_reset(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.ZFlag = True
		cpu.xorA(1)
		self.assertNotEqual(0, cpu.A)
		self.assertFalse(cpu.ZFlag)

	def test_xor_A_resets_C_flag(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.CFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.CFlag)

	def test_xor_A_resets_N_flag(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.NFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.NFlag)

	def test_xor_A_resets_H_flag(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.HFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.HFlag)

	def test_xor_A_sets_S_if_result_is_negative(self):
		cpu = CPU(None)
		cpu.A = 0x96
		cpu.C = 0x5D
		cpu.SFlag = False
		cpu.xorA(1)
		self.assertTrue(cpu.SFlag)

	def test_xor_A_resets_S_if_result_is_positive(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x55
		cpu.SFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.SFlag)

	def test_xor_A_sets_PV_if_parity_even(self):
		cpu = CPU(None)
		cpu.A = 0x44
		cpu.C = 0x11
		cpu.PVFlag = False
		cpu.xorA(1)
		self.assertTrue(cpu.PVFlag)

	def test_xor_A_resets_PV_if_parity_odd(self):
		cpu = CPU(None)
		cpu.A = 0x45
		cpu.C = 0x11
		cpu.PVFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.PVFlag)

	def test_HL_property_assign_correct_values_to_H_and_L(self):
		cpu = CPU(None)
		cpu.HL = 0x1123
		self.assertEqual(0x11, cpu.H)
		self.assertEqual(0x23, cpu.L)

	def test_HL_property_has_correct_value_when_H_and_L_are_set(self):
		cpu = CPU(None)
		cpu.H = 0x66
		cpu.L = 0x01
		self.assertEqual(0x6601, cpu.HL)

	def test_JP_XX_sets_PC_correctly(self):
		cpu = CPU(FakeRom('\xc3\xcb\x11'))
		cpu.pc = 0
		cpu.jp(00)
		self.assertEqual(0x11cb, cpu.pc)

if __name__ == '__main__':
	unittest.main()