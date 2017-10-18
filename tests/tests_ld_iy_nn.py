import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_iy_nn(unittest.TestCase):
	''' FD 21 n n '''
	def test_ld_iy_nn_correctly_copies_nn_value_to_iy(self):
		cpu = CPU(FakeRom('\xFD\x21\x33\x77'))
		cpu.readOp()
		self.assertEqual(0x7733, cpu.IY)

	def test_ld_iy_nn_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xfd\x21\x33\x77'))
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
