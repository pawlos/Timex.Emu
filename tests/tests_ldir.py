import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ldir(unittest.TestCase):

	def test_ldir(self):
		cpu = CPU(FakeRom('\xed\xb0'))
		cpu.HL = 0x1111
		cpu.DE = 0x2222
		cpu.BC = 0x03
		cpu.ram.storeAddr(0x1111, 0x88)
		cpu.ram.storeAddr(0x1112, 0x36)
		cpu.ram.storeAddr(0x1113, 0xA5)
		cpu.ram.storeAddr(0x2222, 0x66)
		cpu.ram.storeAddr(0x2223, 0x59)
		cpu.ram.storeAddr(0x2224, 0xc5)
		cpu.readOp();
		self.assertEqual(0x1114, cpu.HL)
		self.assertEqual(0x2225, cpu.DE)
		self.assertEqual(0x0000, cpu.BC)

		self.assertEqual(0x88, cpu.ram.readAddr(0x1111))
		self.assertEqual(0x36, cpu.ram.readAddr(0x1112))
		self.assertEqual(0xa5, cpu.ram.readAddr(0x1113))

		self.assertEqual(0x88, cpu.ram.readAddr(0x2222))
		self.assertEqual(0x36, cpu.ram.readAddr(0x2223))
		self.assertEqual(0xa5, cpu.ram.readAddr(0x2224))