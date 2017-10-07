import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_r_iy(unittest.TestCase):
	
	def test_ld_a_iy_correctly_copies_value_to_a(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x7e\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.A)

	def test_ld_b_iy_correctly_copies_value_to_b(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x46\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.B)

	def test_ld_c_iy_correctly_copies_value_to_c(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x4e\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.C)

	def test_ld_d_iy_correctly_copies_value_to_d(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x56\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.D)

	def test_ld_e_iy_correctly_copies_value_to_e(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x5e\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.E)

	def test_ld_h_iy_correctly_copies_value_to_h(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x66\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.H)

	def test_ld_l_iy_correctly_copies_value_to_l(self):
		ram = FakeRam([None]*0x2600)
		ram.storeAddr(0x25af+0x19, 0x39)
		cpu = CPU(FakeRom('\xFD\x6e\x19'), ram)
		cpu.IY = 0x25AF
		cpu.readOp()
		self.assertEqual(0x39, cpu.L)