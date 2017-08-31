import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
import tests_sbc


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
		ram = FakeRam([None]*0x2223)
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

	def test_ix_set_get(self):
		cpu = CPU(None)
		cpu.IX = 0x1223;
		self.assertEqual(0x1223, cpu.IX)

	def test_iy_set_get(self):
		cpu = CPU(None)
		cpu.IY = 0x3456;
		self.assertEqual(0x3456, cpu.IY)

def suite():
	return unittest.TestLoader().discover(".", pattern="*.py")

if __name__ == '__main__':
	unittest.TextTestRunner().run(suite())