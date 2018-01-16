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

	def test_rst_8_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xcf'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x08, cpu.PC)

	def test_rst_10_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xd7'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x10, cpu.PC)

	def test_rst_20_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xe7'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x20, cpu.PC)

	def test_rst_28_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xef'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x28, cpu.PC)

	def test_rst_30_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xf7'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x30, cpu.PC)

	def test_rst_38_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		cpu = CPU(FakeRom('\x00'*0x15b3+'\xff'), ram)
		cpu.PC = 0x15B3
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x38, cpu.PC)