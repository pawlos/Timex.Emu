import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_rst(unittest.TestCase):

	def test_rst_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xdf'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x18, cpu.PC)

	def test_rst_0_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xc7'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x0, cpu.PC)