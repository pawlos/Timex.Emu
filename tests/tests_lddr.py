import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestAdd(unittest.TestCase):

	def test_lddr(self):
		cpu = CPU(FakeRom('\xed\xb8'))
		cpu.HL = 0x1114
		cpu.DE = 0x2225
		cpu.BC = 0x03
		cpu.ram.storeAddr(0x1114, 0xA5)
		cpu.ram.storeAddr(0x1113, 0x36)
		cpu.ram.storeAddr(0x1112, 0x88)
		cpu.ram.storeAddr(0x2225, 0xc5)
		cpu.ram.storeAddr(0x2224, 0x59)
		cpu.ram.storeAddr(0x2223, 0x66)
		cpu.readOp();
		self.assertEqual(0x1111, cpu.HL)
		self.assertEqual(0x2222, cpu.DE)
		self.assertEqual(0x0000, cpu.BC)

		self.assertEqual(0xA5, cpu.ram.readAddr(0x1114))
		self.assertEqual(0x36, cpu.ram.readAddr(0x1113))
		self.assertEqual(0x88, cpu.ram.readAddr(0x1112))

		self.assertEqual(0xA5, cpu.ram.readAddr(0x2225))
		self.assertEqual(0x36, cpu.ram.readAddr(0x2224))
		self.assertEqual(0x88, cpu.ram.readAddr(0x2223))

	def test_lddr_does_set_flags_correctly(self):
		cpu = CPU(FakeRom('\xed\xb8'))
		cpu.HL = 0x1114
		cpu.DE = 0x2225
		cpu.BC = 0x03
		cpu.HFlag = True
		cpu.NFlag = True
		cpu.PVFlag = True
		cpu.SFlag = False
		cpu.ZFlag = True
		cpu.ram.storeAddr(0x1114, 0xA5)
		cpu.ram.storeAddr(0x1113, 0x36)
		cpu.ram.storeAddr(0x1112, 0x88)
		cpu.ram.storeAddr(0x2225, 0xc5)
		cpu.ram.storeAddr(0x2224, 0x59)
		cpu.ram.storeAddr(0x2223, 0x66)
		cpu.readOp();	
		self.assertFalse(cpu.HFlag)
		self.assertFalse(cpu.NFlag)
		self.assertFalse(cpu.PVFlag)
		self.assertFalse(cpu.SFlag)
		self.assertTrue(cpu.ZFlag)