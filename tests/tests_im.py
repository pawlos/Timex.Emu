import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_im1(unittest.TestCase):
	def test_im1_interrupt_restart_execution_at_given_address(self):
		cpu = CPU(FakeRom('\xed\x56'))
		cpu.readOp()
		#generate interrupt
		self.assertEqual(0x0038, cpu.PC)

	def test_im1_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xed\x56'))
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