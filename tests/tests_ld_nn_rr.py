import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ld_nn_rr(unittest.TestCase):

	def test_ed43nn_correctly_stores_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x43\x10\x00'))
		cpu.BC = 0x4644
		cpu.readOp()
		self.assertEqual(0x46, cpu.ram[0x1001])
		self.assertEqual(0x44, cpu.ram[0x1000])

	def test_ed63nn_correctly_stores_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x63\x10\x00'))
		cpu.HL = 0x4644
		cpu.readOp()
		self.assertEqual(0x46, cpu.ram[0x1001])
		self.assertEqual(0x44, cpu.ram[0x1000])

	def test_ed73nn_correctly_stores_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x73\x10\x00'))
		cpu.SP = 0x4644
		cpu.readOp()
		self.assertEqual(0x46, cpu.ram[0x1001])
		self.assertEqual(0x44, cpu.ram[0x1000])

	def test_ed43nn_does_not_affect_flags(self):
		cpu = CPU(FakeRom('\xed\x43\x10\x00'))
		cpu.CFlag = True
		cpu.ZFlag = False
		cpu.SFlag = True
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.CFlag)
		self.assertFalse(cpu.ZFlag)
		self.assertTrue(cpu.SFlag)
		self.assertFalse(cpu.HFlag)

	def test_ed53nn_correctly_stores_de_value_at_given_location(self):
		cpu = CPU(FakeRom('\xed\x53\x10\x00'))
		cpu.DE = 0xabba
		cpu.readOp()
		self.assertEqual(0xab, cpu.ram[0x1001])
		self.assertEqual(0xba, cpu.ram[0x1000])

	def test_ed53nn_takes_6_m_cycles(self):
		cpu = CPU(FakeRom('\xed\x53\x10\x00'))
		cpu.DE = 0xabba
		cpu.readOp()
		self.assertEqual(6, cpu.m_cycles)

	def test_ed53nn_takes_20_t_states(self):
		cpu = CPU(FakeRom('\xed\x53\x10\x00'))
		cpu.DE = 0xabba
		cpu.readOp()
		self.assertEqual(20, cpu.t_states)