import unittest

from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_xor_a(unittest.TestCase):
	def test_xor_A_works_correctly(self):
		cpu = CPU(ROM('\xa8'))
		cpu.A = 12
		cpu.B = 11
		cpu.readOp()
		self.assertEqual(7, cpu.A)

	def test_if_A_is_set_to_96H_xor_5DH_works(self):
		cpu = CPU(ROM('\xa8'))
		cpu.A = 0x96
		cpu.B = 0x5D
		cpu.readOp()
		self.assertEqual(0xCB, cpu.A)

	def test_if_A_xors_to_zero_Z_is_set(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.readOp()
		self.assertEqual(0, cpu.A)
		self.assertEqual(True, cpu.ZFlag)

	def test_if_A_xors_to_non_zero_Z_is_reset(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.ZFlag = True
		cpu.readOp()
		self.assertNotEqual(0, cpu.A)
		self.assertFalse(cpu.ZFlag)

	def test_xor_A_resets_C_flag(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x12
		cpu.CFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_xor_A_resets_N_flag(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_xor_A_resets_H_flag(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x13
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_xor_A_sets_S_if_result_is_negative(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x96
		cpu.C = 0x5D
		cpu.SFlag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_xor_A_resets_S_if_result_is_positive(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x12
		cpu.C = 0x55
		cpu.SFlag = True
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_xor_A_sets_PV_if_parity_even(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x44
		cpu.C = 0x11
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_xor_A_resets_PV_if_parity_odd(self):
		cpu = CPU(ROM('\xa9'))
		cpu.A = 0x45
		cpu.C = 0x11
		cpu.PVFlag = True
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)

	def test_xor_a_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xa8'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_xor_a_takes_4_t_states(self):
		cpu = CPU(ROM('\xa8'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)