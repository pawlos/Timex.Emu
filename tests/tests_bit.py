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

	def test_bit_IY_plus_30_reset_correctly_bit(self):
		ram = FakeRam([None]*0x2032)
		ram.storeAddr(0x2030, 0b00001111)
		cpu = CPU(FakeRom('\xfd\xcb\x30\x8e'), ram)
		cpu.IY = 0x2000
		cpu.readOp()
		self.assertEquals(0b1101, ram.readAddr(0x2030))

	def test_bit_plus_x_takes_6_m_cycles(self):
		ram = FakeRam([None]*0x2032)
		ram.storeAddr(0x2001, 0b00001111)
		cpu = CPU(FakeRom('\xfd\xcb\x01\xce'), ram)
		cpu.IY = 0x2000
		cpu.readOp()
		self.assertEquals(6, cpu.m_cycles)

	def test_bit_plus_x_takes_20_t_states(self):
		ram = FakeRam([None]*0x2032)
		ram.storeAddr(0x2001, 0b00001111)
		cpu = CPU(FakeRom('\xfd\xcb\x01\xce'), ram)
		cpu.IY = 0x2000
		cpu.readOp()
		self.assertEquals(23, cpu.t_states)

	def test_bit_IY_plus_30_takes_6_m_cycles(self):
		ram = FakeRam([None]*0x2032)
		ram.storeAddr(0x2030, 0b00001111)
		cpu = CPU(FakeRom('\xfd\xcb\x30\x8e'), ram)
		cpu.IY = 0x2000
		cpu.readOp()
		self.assertEquals(6, cpu.m_cycles)

	def test_bit_IY_plus_30_takes_23_t_states(self):
		ram = FakeRam([None]*0x2032)
		ram.storeAddr(0x2030, 0b00001111)
		cpu = CPU(FakeRom('\xfd\xcb\x30\x8e'), ram)
		cpu.IY = 0x2000
		cpu.readOp()
		self.assertEquals(23, cpu.t_states)

	def test_bit_IY_plus_4_takes_5_m_cycles(self):
		ram = FakeRam([None]*0x2005)
		ram.storeAddr(0x2004, 1 << 6)
		cpu = CPU(FakeRom('\xfd\xcb\x04\x76'), ram)
		cpu.ZFlag = Bits.reset()
		cpu.IY = 0x2000
		cpu.readOp();
		self.assertEquals(5, cpu.m_cycles)

	def test_bit_IY_plus_4_takes_20_t_states(self):
		ram = FakeRam([None]*0x2005)
		ram.storeAddr(0x2004, 1 << 6)
		cpu = CPU(FakeRom('\xfd\xcb\x04\x76'), ram)
		cpu.ZFlag = Bits.reset()
		cpu.IY = 0x2000
		cpu.readOp();
		self.assertEquals(20, cpu.t_states)
