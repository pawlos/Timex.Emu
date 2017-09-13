import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class TestBIT(unittest.TestCase):

	def test_bit_IY_plus_4_set_correctly_set_z_flag(self):
		ram = FakeRam([None]*0x2005)
		ram.storeAddr(0x2004, 1 << 6)
		cpu = CPU(FakeRom('\xfd\xcb\x04\x76'), ram)
		cpu.ZFlag = Bits.reset()
		cpu.IY = 0x2000
		cpu.readOp();
		self.assertTrue(cpu.ZFlag)