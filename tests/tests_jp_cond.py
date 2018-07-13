import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_jp_cond(unittest.TestCase):

	def test_jp_c_jumps_if_CFlag_is_set(self):
		cpu = CPU(ROM('\xDA\x20\x15'))
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_c_jumps_if_CFlag_is_not_set(self):
		cpu = CPU(ROM('\xD2\x20\x15'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_z_jumps_if_ZFlag_is_not_set(self):
		cpu = CPU(ROM('\xC2\x20\x15'))
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_z_jumps_if_ZFlag_is_set(self):
		cpu = CPU(ROM('\xCA\x20\x15'))
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_po_jumps_if_PVFlag_is_not_set(self):
		cpu = CPU(ROM('\xe2\x20\x15'))
		cpu.PVFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_po_jumps_if_PVFlag_is_set(self):
		cpu = CPU(ROM('\xea\x20\x15'))
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_s_jumps_if_SFlag_is_not_set(self):
		cpu = CPU(ROM('\xF2\x20\x15'))
		cpu.SFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_s_jumps_if_SFlag_is_set(self):
		cpu = CPU(ROM('\xFA\x20\x15'))
		cpu.SFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_s_takes_3_m_cycles(self):
		cpu = CPU(ROM('\xFA\x20\x15'))
		cpu.SFlag = True
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_jp_po_takes_10_t_states(self):
		cpu = CPU(ROM('\xea\x20\x15'))
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(10, cpu.t_states)
