import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_sp_hl(unittest.TestCase):

	def test_ld_sp_hl_correctly_copies_hl_value_to_sp(self):
		cpu = CPU(FakeRom('\xf9'))
		cpu.HL = 0xadda
		cpu.readOp()
		self.assertEqual(0xadda, cpu.SP)

	def test_ld_sp_hl_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xf9'))
		cpu.ZFlag = True
		cpu.PVFlag = False
		cpu.HFlag = True
		cpu.NFlag = False
		cpu.SFlag = True
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)
		self.assertFalse(cpu.PVFlag)
		self.assertTrue(cpu.HFlag)
		self.assertFalse(cpu.NFlag)
		self.assertTrue(cpu.SFlag)
