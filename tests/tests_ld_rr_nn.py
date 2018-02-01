import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_rr_nn(unittest.TestCase):

	def test_ld_BC_nn_correctly_stores_value_to_BC(self):
		cpu = CPU(FakeRom('\x01\xba\xab'))
		cpu.readOp()
		self.assertEqual(0xabba, cpu.BC)

	def test_ld_DE_nn_correctly_stores_value_to_DE(self):
		cpu = CPU(FakeRom('\x11\xde\xc0'))
		cpu.readOp()
		self.assertEqual(0xc0de, cpu.DE)

	def test_ld_HL_nn_correctly_stores_value_to_HL(self):
		cpu = CPU(FakeRom('\x21\xfe\xca'))
		cpu.readOp()
		self.assertEqual(0xcafe, cpu.HL)

	def test_ld_SP_nn_correctly_stores_value_to_SP(self):
		cpu = CPU(FakeRom('\x31\x37\x13'))
		cpu.readOp()
		self.assertEqual(0x1337, cpu.SP)

	def test_ld_BC_addr_nn_correctly_loads_value_to_BC(self):
		ram = FakeRam([None]*0x2132)
		ram.storeAddr(0x2130, 0x65)
		ram.storeAddr(0x2131, 0x78)
		cpu = CPU(FakeRom('\xED\x4b\x30\x21'),ram)
		cpu.readOp()
		self.assertEqual(0x7865, cpu.BC)

	def test_ld_DE_addr_nn_correctly_loads_value_to_DE(self):
		ram = FakeRam([None]*0x2132)
		ram.storeAddr(0x2130, 0x65)
		ram.storeAddr(0x2131, 0x78)
		cpu = CPU(FakeRom('\xED\x5b\x30\x21'),ram)
		cpu.readOp()
		self.assertEqual(0x7865, cpu.DE)

	def test_ld_HL_addr_nn_correctly_loads_value_to_HL(self):
		ram = FakeRam([None]*0x2132)
		ram.storeAddr(0x2130, 0x65)
		ram.storeAddr(0x2131, 0x78)
		cpu = CPU(FakeRom('\xED\x6b\x30\x21'),ram)
		cpu.readOp()
		self.assertEqual(0x7865, cpu.HL)
