import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_nn_hl(unittest.TestCase):

	def test_ld_nn_a_correctly_stores_value_at_given_address(self):
		cpu = CPU(FakeRom('\x32\x31\x41'))
		cpu.A = 0xD7
		cpu.readOp()
		self.assertEqual(0xD7, cpu.ram.readAddr(0x3141))

	def test_ld_nn_a_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\x32\xb2\x29'))
		cpu.HFlag = False
		cpu.ZFlag = True
		cpu.PVFlag = False
		cpu.SFlag = True

		self.assertFalse(cpu.HFlag)
		self.assertTrue(cpu.ZFlag)
		self.assertFalse(cpu.PVFlag)
		self.assertTrue(cpu.SFlag)