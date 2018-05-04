import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_exx(unittest.TestCase):
	def test_exx_echanges_16_bit_bc_de_hl_registers(self):
		cpu = CPU(FakeRom('\xd9'))
		cpu.BC = 0x445a
		cpu.DE = 0x3da2
		cpu.HL = 0x8859
		cpu.BCPrim = 0x0988
		cpu.DEPrim = 0x9300
		cpu.HLPrim = 0x00e7
		cpu.readOp()

		self.assertEqual(0x0988, cpu.BC)
		self.assertEqual(0x9300, cpu.DE)
		self.assertEqual(0x00e7, cpu.HL)
		self.assertEqual(0x445a, cpu.BCPrim)
		self.assertEqual(0x3da2, cpu.DEPrim)
		self.assertEqual(0x8859, cpu.HLPrim)

	def test_exx_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xd9'))
		cpu.ZFlag = True
		cpu.SFlag = False
		cpu.PVFlag = True
		cpu.HFlag = True
		cpu.NFlag = True
		cpu.readOp()
		
		self.assertTrue(cpu.ZFlag)
		self.assertFalse(cpu.SFlag)
		self.assertTrue(cpu.PVFlag)
		self.assertTrue(cpu.HFlag)
		self.assertTrue(cpu.NFlag)

	def test_exx_takes_1_m_cycle(self):
		cpu = CPU(FakeRom('\xd9'))
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_exx_takes_4_t_states(self):
		cpu = CPU(FakeRom('\xd9'))
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)