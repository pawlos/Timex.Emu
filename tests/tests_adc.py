import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import *

class tests_adc(unittest.TestCase):

	def test_add_HL_BC_with_C_flag_unset_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x4a'))
		cpu.HL = 0xCDCD
		cpu.BC = 0x1111
		cpu.CFlag = Bits.reset()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111,cpu.HL)


	def test_add_HL_BC_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x4a'))
		cpu.HL = 0xCDCD
		cpu.BC = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111+0x1,cpu.HL)

	def test_add_HL_DE_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x5a'))
		cpu.HL = 0xCDCD
		cpu.DE = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0XCDCD+0x1111+0x1,cpu.HL)

	def test_add_HL_DE_with_C_flag_set_correctly_calculates_value(self):
		cpu = CPU(FakeRom('\xed\x6a'))
		cpu.HL = 0x1111
		cpu.CFlag = Bits.set()
		cpu.readOp()
		self.assertEqual(0x1111+0x1111+0x1,cpu.HL)