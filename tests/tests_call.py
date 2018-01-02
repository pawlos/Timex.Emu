import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_call(unittest.TestCase):

	def test_call(self):
		ram = FakeRam([None]*0x3002)
		
		rom = FakeRom('\x00'*0x1A47+'\xcd\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram.readAddr(0x3001))
		self.assertEqual(0x4A, cpu.ram.readAddr(0x3000))
