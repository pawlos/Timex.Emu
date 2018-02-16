import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_ret(unittest.TestCase):

	def test_ret_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x2002)
		ram.storeAddr(0x2000, 0xB5)
		ram.storeAddr(0x2001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc9'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x2000
		cpu.readOp();
		self.assertEqual(0x18B5, cpu.PC)
		self.assertEqual(0x2002, cpu.SP)


	def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_reset(self):
		ram = FakeRam([None]*0x2002)
		ram.storeAddr(0x2000, 0xB5)
		ram.storeAddr(0x2001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x2000
		cpu.ZFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x18B5, cpu.PC)
		self.assertEqual(0x2002, cpu.SP)


	def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_set(self):
		ram = FakeRam([None]*0x2002)
		ram.storeAddr(0x2000, 0xB5)
		ram.storeAddr(0x2001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x2000
		cpu.ZFlag = Bits.set()
		cpu.readOp();
		self.assertEqual(0x3536, cpu.PC)
		self.assertEqual(0x2000, cpu.SP)