import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_rld(unittest.TestCase):

	def test_rld_does_modify_value_correctly(self):
		ram = FakeRam([0x00]*0x5001)
		ram.storeAddr(0x5000, 0b00110001)
		cpu = CPU(FakeRom('\xed\x6f'), ram)
		cpu.A = 0b01111010
		cpu.HL = 0x5000
		cpu.readOp();
		self.assertEqual(0b01110011, cpu.A)
		self.assertEqual(0b00011010, cpu.ram.readAddr(cpu.HL))