import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_nn_rr(unittest.TestCase):

	def test_ed43nn_correctly_stores_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x43\x10\x00'))
		cpu.BC = 0x4644
		cpu.readOp()
		self.assertEqual(cpu.ram.readAddr(0x1000), 0x46)
		self.assertEqual(cpu.ram.readAddr(0x1001), 0x44)

	def test_ed43nn_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xed\x43\x10\x00'))
		cpu.CFlag = True
		cpu.ZFlag = False
		cpu.PVFlag = None
		cpu.SFlag = True
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)
		self.assertFalse(cpu.ZFlag)
		self.assertEqual(None, cpu.PVFlag)
		self.assertTrue(cpu.SFlag)
		self.assertFalse(cpu.HFlag)

	def test_ed53nn_correctly_stores_de_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x53\x10\x00'))
		cpu.DE = 0xabba
		cpu.readOp()
		self.assertEqual(cpu.ram.readAddr(0x1000), 0xab)
		self.assertEqual(cpu.ram.readAddr(0x1001), 0xba)