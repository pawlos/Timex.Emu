import unittest
from cpu import CPU


class TestCPUFunctions(unittest.TestCase):
	def test_init_zeros_registers(self):
		cpu = CPU(None)
		self.assertEqual(0, cpu.A)
		self.assertEqual(0, cpu.B)
		self.assertEqual(0, cpu.C)
		self.assertEqual(0, cpu.registerD())
		self.assertEqual(0, cpu.registerE())
		self.assertEqual(0, cpu.registerH())
		self.assertEqual(0, cpu.registerL())

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

	def test_Xor_A_resets_C_flag(self):
		cpu = CPU(None)
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.CFlag = True
		cpu.xorA(1)
		self.assertFalse(cpu.CFlag)


if __name__ == '__main__':
	unittest.main()