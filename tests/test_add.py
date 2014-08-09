import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestAdd(unittest.TestCase):

	def test_add_hl_de_returns_correct_result(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0xabba, cpu.HL)


	def test_add_hl_de_does_not_change_s_flag(self):
		cpu = CPU(FakeRom('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.SFlag = False
		cpu.readOp()
		self.assertFalse(cpu.SFlag)
		cpu.SFlag = True
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_add_hl_de_does_not_change_z_flag(self):
		cpu = CPU(FakeRom('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.ZFlag = True
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)
		cpu.ZFlag = False
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_add_hl_de_does_not_change_pv_flag(self):
		cpu = CPU(FakeRom('\x19\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.PVFlag = False
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)
		cpu.PVFlag = True
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_add_hl_de_resets_n_flag(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0xb0b0
		cpu.DE = 0x0a0a
		cpu.NFlag = True
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_add_hl_de_sets_c_if_carry_from_bit_15(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0xf000
		cpu.DE = 0x1000
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_hl_de_resets_c_flag_if_carry_does_not_occur(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0xf000
		cpu.DE = 0x0fff
		cpu.CFlag = True
		cpu.readOp()
		self.assertFalse(cpu.CFlag)

	def test_add_hl_de_sets_h_flag_if_carry_from_bit_11(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0x0f00
		cpu.DE = 0x0100
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_add_hl_de_resets_h_flag_if_carry_from_bit_11_does_not_occur(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0x0f00
		cpu.DE = 0x00ff
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)
