import unittest
from cpu import CPU


class TestCPUFunctions(unittest.TestCase):
	def test_init_zeros_registers(self):
		cpu = CPU(None)
		self.assertEqual(0, cpu.A)
		self.assertEqual(0, cpu.B)
		self.assertEqual(0, cpu.registerC())
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


if __name__ == '__main__':
	unittest.main()