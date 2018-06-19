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

	def test_ld_iy_d_n_correctly_copies_n_value_to_iy_plus_d(self):
		ram = FakeRam([None]*0x2000)
		cpu = CPU(FakeRom('\xFD\x36\x01\x77'))
		cpu.IY = 0x1111
		cpu.readOp()
		self.assertEqual(0x77, cpu.ram.readAddr(0x1112))

	def test_ld_iy_d_n_takes_5_m_cycle(self):
		ram = FakeRam([None]*0x2000)
		cpu = CPU(FakeRom('\xFD\x36\x01\x77'))
		cpu.IY = 0x1111
		cpu.readOp()
		self.assertEqual(5, cpu.m_cycles)

	def test_ld_iy_d_n_takes_19_t_states(self):
		ram = FakeRam([None]*0x2000)
		cpu = CPU(FakeRom('\xFD\x36\x01\x77'))
		cpu.IY = 0x1111
		cpu.readOp()
		self.assertEqual(19, cpu.t_states)

	def test_ld_iy_nn_takes_4_m_cycles(self):
		cpu = CPU(FakeRom('\xFD\x21\x33\x77'))
		cpu.readOp()
		self.assertEqual(4, cpu.m_cycles)

	def test_ld_iy_nn_takes_14_t_states(self):
		cpu = CPU(FakeRom('\xFD\x21\x33\x77'))
		cpu.readOp()
		self.assertEqual(14, cpu.t_states)