import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class cp_h(unittest.TestCase):

	def test_cp_H_sets_ZF_if_H_is_equal_to_0(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 3
		cpu.H = 3
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_cp_H_resets_ZF_if_H_is_not_equal_to_0(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 1
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_cp_H_sets_SF_if_H_is_negative(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 1
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_cp_H_sets_NF_always(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.H = 0
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_cp_H_sets_CF_is_results_goes_below_zero(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 3
		cpu.H = 0xff
		cpu.readOp();
		self.assertTrue(cpu.CFlag)

	def test_cp_H_sets_HF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x10
		cpu.H = 0x01
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_cp_H_resets_HF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x3
		cpu.H = 0x1
		cpu.readOp()
		self.assertFalse(cpu.HFlag)

	def test_cp_H_sets_PVF(self):
		cpu = CPU(FakeRom('\xbc'))
		cpu.A = 0x7f
		cpu.H = 0x81
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)