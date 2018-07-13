import unittest

from cpu import CPU
from rom import ROM
from opcodes import Opcodes
from loggers import Logger

class tests_ld_sp_hl(unittest.TestCase):

	def test_ld_sp_hl_correctly_copies_hl_value_to_sp(self):
		cpu = CPU(ROM('\xf9'))
		cpu.HL = 0xadda
		cpu.readOp()
		self.assertEqual(0xadda, cpu.SP)

	def test_ld_sp_hl_does_not_affect_flags(self):
		cpu = CPU(ROM('\xf9'))
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

	def test_ld_sp_hl_does_takes_1_m_cycles(self):
		cpu = CPU(ROM('\xf9'))
		cpu.HL = 0xadda
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_ld_sp_hl_takes_6_t_states(self):
		cpu = CPU(ROM('\xf9'))
		cpu.HL = 0xadda
		cpu.readOp()
		self.assertEqual(6, cpu.t_states)
