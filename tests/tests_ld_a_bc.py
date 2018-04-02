import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_a_bc(unittest.TestCase):

	def test_ld_a_bc_loads_corect_value(self):
		ram = FakeRam([0x00]*0x5000)
		ram.storeAddr(0x4747, 0x12)
		cpu = CPU(FakeRom('\x0a'), ram)
		cpu.BC = 0x4747
		cpu.readOp();
		self.assertEqual(0x12, cpu.A)

	def test_ld_a_bc_takes_2_m_cycles(self):
		ram = FakeRam([0x00]*0x5000)
		ram.storeAddr(0x4747, 0x12)
		cpu = CPU(FakeRom('\x0a'), ram)
		cpu.BC = 0x4747
		cpu.readOp();
		self.assertEqual(2,cpu.m_cycles)

	def test_ld_a_bc_takes_7_t_states(self):
		ram = FakeRam([0x00]*0x5000)
		ram.storeAddr(0x4747, 0x12)
		cpu = CPU(FakeRom('\x0a'), ram)
		cpu.BC = 0x4747
		cpu.readOp();
		self.assertEqual(7,cpu.t_states)