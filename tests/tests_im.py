import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_im(unittest.TestCase):
	def test_im1_interrupt_restart_execution_at_given_address(self):
		cpu = CPU(FakeRom('\xed\x56'))
		cpu.readOp()
		#generate interrupt
		cpu.generateInterrupt()
		self.assertEqual(0x0038, cpu.PC)

	def test_im0_sets_interrupt_mode_to_0(self):
		cpu = CPU(FakeRom('\xed\x46'))
		cpu.readOp()
		self.assertEqual(0x00, cpu.interruptMode)

	def test_im2_sets_interrupt_mode_to_2(self):
		cpu = CPU(FakeRom('\xed\x5e'))
		cpu.readOp()
		self.assertEqual(0x02, cpu.interruptMode)

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

	def test_im1_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x56'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_im1_takes_8_t_states(self):
		cpu = CPU(FakeRom('\xed\x56'))
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)

	def test_im2_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x5e'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_im2_takes_8_t_states(self):
		cpu = CPU(FakeRom('\xed\x5e'))
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)

	def test_im0_takes_2_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x46'))
		cpu.readOp()
		self.assertEqual(2, cpu.m_cycles)

	def test_im0_takes_8_t_states(self):
		cpu = CPU(FakeRom('\xed\x46'))
		cpu.readOp()
		self.assertEqual(8, cpu.t_states)