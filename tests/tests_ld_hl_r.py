import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_hl_addr(unittest.TestCase):

	def test_ld_hl_A_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x77'), ram)
		cpu.HL = 0x2000
		cpu.A = 0x34
		cpu.readOp()
		self.assertEqual(0x34, ram.readAddr(0x2000))

	def test_ld_hl_B_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x70'), ram)
		cpu.HL = 0x2000
		cpu.B = 0x34
		cpu.readOp()
		self.assertEqual(0x34, ram.readAddr(0x2000))

	def test_ld_hl_C_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x71'), ram)
		cpu.HL = 0x2000
		cpu.C = 0x34
		cpu.readOp()
		self.assertEqual(0x34, ram.readAddr(0x2000))

	def test_ld_hl_D_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x72'), ram)
		cpu.HL = 0x2000
		cpu.D = 0x34
		cpu.readOp()
		self.assertEqual(0x34, ram.readAddr(0x2000))

	def test_ld_hl_E_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x73'), ram)
		cpu.HL = 0x2000
		cpu.E = 0x20
		cpu.readOp()
		self.assertEqual(0x20, ram.readAddr(0x2000))

	def test_ld_hl_H_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x74'), ram)
		cpu.HL = 0x2000
		cpu.readOp()
		self.assertEqual(0x20, ram.readAddr(0x2000))

	def test_ld_hl_L_correctly_stores_value_from_given_address_to_hl(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x75'), ram)
		cpu.HL = 0x2000
		cpu.readOp()
		self.assertEqual(0x00, ram.readAddr(0x2000))

	def test_ld_hl_L_takes_2_m_cycles(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x75'), ram)
		cpu.HL = 0x2000
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_ld_hl_L_takes_7_t_states(self):
		ram = FakeRam([None]*0x2001)
		cpu = CPU(FakeRom('\x75'), ram)
		cpu.HL = 0x2000
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)
