import unittest
from cpu import CPU


class TestCPUFunctions(unittest.TestCase):
	def test_init_zeros_registers(self):
		cpu = CPU(None)
		self.assertEqual(0, cpu.registerA())
		self.assertEqual(0, cpu.registerB())
		self.assertEqual(0, cpu.registerC())
		self.assertEqual(0, cpu.registerD())
		self.assertEqual(0, cpu.registerE())
		self.assertEqual(0, cpu.registerH())
		self.assertEqual(0, cpu.registerL())


if __name__ == '__main__':
	unittest.main()