import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestRRD(unittest.TestCase):

	def test_rrd_does_modify_value_correctly(self):
		ram = FakeRam([0x00]*0x5001)
		ram.storeAddr(0x5000, 0b00100000)
		cpu = CPU(FakeRom('\xed\x67'), ram)
		cpu.A = 0b10000100
		cpu.HL = 0x5000
		cpu.readOp();
		self.assertEqual(0b10000000, cpu.A)
		self.assertEqual(0b01000010, cpu.ram.readAddr(cpu.HL))