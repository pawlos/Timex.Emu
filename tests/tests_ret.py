import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_ret(unittest.TestCase):

	def test_ret_does_sets_PC_correctly(self):
		ram = FakeRam([None]*0x8000)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc9'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.readOp();
		self.assertEqual(0x18B5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)


	def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_reset(self):
		ram = FakeRam([None]*0x8000)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.ZFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x18B5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)


	def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_set(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.ZFlag = Bits.set()
		cpu.readOp();
		self.assertEqual(0x3536, cpu.PC)
		self.assertEqual(0x4000, cpu.SP)

	def test_ret_z_does_sets_PC_correctly_if_Zflag_is_set(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc8'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.ZFlag = Bits.set()
		cpu.readOp();
		self.assertEqual(0x18B5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)

	def test_ret_z_does_sets_PC_correctly_if_Zflag_is_reset(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xc8'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.ZFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x3536, cpu.PC)
		self.assertEqual(0x4000, cpu.SP)

	def test_ret_nc_does_sets_PC_correctly_if_Cflag_is_reset(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xd0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.CFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x18b5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)

	def test_ret_c_does_sets_PC_correctly_if_Cflag_is_set(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xd8'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.CFlag = Bits.set()
		cpu.readOp();
		self.assertEqual(0x18b5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)

	def test_ret_po_does_sets_PC_correctly_if_PVflag_is_reset(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xe0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.PVFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x18b5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)

	def test_ret_po_does_sets_PC_correctly_if_PVflag_is_set(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xe8'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.PVFlag = Bits.set()
		cpu.readOp();
		self.assertEqual(0x18b5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)

	def test_ret_p_does_sets_PC_correctly_if_PVflag_is_reset(self):
		ram = FakeRam([None]*0x8002)
		ram.storeAddr(0x4000, 0xB5)
		ram.storeAddr(0x4001, 0x18)
		cpu = CPU(FakeRom('\x00'*0x3535+'\xf0'), ram)
		cpu.PC = 0x3535
		cpu.SP = 0x4000
		cpu.SFlag = Bits.reset()
		cpu.readOp();
		self.assertEqual(0x18b5, cpu.PC)
		self.assertEqual(0x4002, cpu.SP)