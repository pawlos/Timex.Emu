import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_jp_cond(unittest.TestCase):

	def test_jp_c_jumps_if_CFlag_is_set(self):
		cpu = CPU(FakeRom('\xDA\x20\x15'))
		cpu.CFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_c_jumps_if_CFlag_is_not_set(self):
		cpu = CPU(FakeRom('\xD2\x20\x15'))
		cpu.CFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_z_jumps_if_ZFlag_is_not_set(self):
		cpu = CPU(FakeRom('\xC2\x20\x15'))
		cpu.ZFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_jp_z_jumps_if_ZFlag_is_set(self):
		cpu = CPU(FakeRom('\xCA\x20\x15'))
		cpu.ZFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)
