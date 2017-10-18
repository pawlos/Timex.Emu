import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_nop(unittest.TestCase):

	def test_nop_does_not_change_hl(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.HL = 0x9999
		cpu.readOp();
		self.assertEqual(0x9999, cpu.HL)

	def test_nop_does_not_change_de(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.DE = 0x8999
		cpu.readOp();
		self.assertEqual(0x8999, cpu.DE)

	def test_nop_does_not_change_bc(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.BC = 0x1223
		cpu.readOp()
		self.assertEqual(0x1223, cpu.BC)

	def test_nop_does_not_change_sp(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.SP = 0x9799
		cpu.readOp()
		self.assertEqual(0x9799, cpu.SP)

	def test_nop_does_not_change_a(self):
		cpu = CPU(FakeRom('\x00'))
		cpu.A = 0x99
		cpu.readOp()
		self.assertEqual(0x99, cpu.A)
