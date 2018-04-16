import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_add_iy(unittest.TestCase):

	def test_add_iy_bc_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x09'))
		cpu.IY = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IY)

	def test_add_iy_de_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x19'))
		cpu.IY = 0x1001
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0x1bb1, cpu.IY)

	def test_add_iy_iy_returns_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x29'))
		cpu.IY = 0x1001
		cpu.readOp()
		self.assertEqual(0x2002, cpu.IY)

	def test_add_iy_sp_retursn_correct_result(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IY = 0x1001
		cpu.SP = 0x0880
		cpu.readOp()
		self.assertEqual(0x1881, cpu.IY)

	def test_add_iy_rr_resets_n_flag(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IY = 0x1001
		cpu.SP = 0x0880
		cpu.NFlag = Bits.set()
		cpu.readOp()
		self.assertFalse(cpu.NFlag)

	def test_add_iy_rr_sets_c_flag_is_results_is_too_big(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IY = 0xFFFF
		cpu.SP = 0x0001
		cpu.CFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)

	def test_add_iy_rr_sets_h_flag_if_carry_from_11th_bit(self):
		cpu = CPU(FakeRom('\xfd\x39'))
		cpu.IY = 0xFFF
		cpu.SP = 0x0001
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_add_iy_a_sets_correct_value(self):
		ram = FakeRam([None]*0x110)
		ram.storeAddr(0x109, 0x11)
		cpu = CPU(FakeRom('\xfd\x86\x09'), ram)
		cpu.IY = 0x100
		cpu.A = 0x11
		cpu.readOp()
		self.assertEqual(0x22, cpu.A)

	def test_add_iy_bc_takes_4_m_cycles(self):
		cpu = CPU(FakeRom('\xfd\x09'))
		cpu.IY = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(4, cpu.m_cycles)

	def test_add_iy_bc_takes_15_t_states(self):
		cpu = CPU(FakeRom('\xfd\x09'))
		cpu.IY = 0x1001
		cpu.BC = 0x0bb0
		cpu.readOp()
		self.assertEqual(15, cpu.t_states)
