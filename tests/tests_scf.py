import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_ccf(unittest.TestCase):

	def test_scf_inverts_c(self):
		cpu = CPU(ROM('\x37'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_scf_takes_1_m_cycles(self):
		cpu = CPU(ROM('\x37'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(1, cpu.m_cycles)

	def test_scf_takes_4_t_states(self):
		cpu = CPU(ROM('\x37'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(4, cpu.t_states)

