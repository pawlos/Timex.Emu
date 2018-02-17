import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_srl(unittest.TestCase):

	def test_srl_h_does_shift_h_correctly(self):
		cpu = CPU(FakeRom('\xcb\x3c'), FakeRam())
		cpu.H = 0b11110000
		cpu.readOp();
		self.assertEqual(0b01111000, cpu.H)


	def test_srl_h_does_set_Cflag_correctly(self):
		cpu = CPU(FakeRom('\xcb\x3c'), FakeRam())
		cpu.H = 0b11110001
		cpu.readOp();
		self.assertTrue(cpu.CFlag)

	