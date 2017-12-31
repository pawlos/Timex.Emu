import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_bit(unittest.TestCase):

	def test_bit_IY_plus_4_set_correctly_set_z_flag(self):
		ram = FakeRam([None]*0x2005)
		ram.storeAddr(0x2004, 1 << 6)
		cpu = CPU(FakeRom('\xfd\xcb\x04\x76'), ram)
		cpu.ZFlag = Bits.reset()
		cpu.IY = 0x2000
		cpu.readOp();
		self.assertTrue(cpu.ZFlag)

	def test_bit_IY_plus_1_set_correctly_the_value(self):
		ram = FakeRam([None]*0x2002)
		ram.storeAddr(0x2001, 0b00001101)
		cpu = CPU(FakeRom('\xfd\xcb\x01\xce'), ram)
		cpu.IY = 0x2000
		cpu.readOp()

		self.assertEquals(0x0F, ram.readAddr(0x2001))