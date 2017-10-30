import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_call_cond(unittest.TestCase):

	def test_call_c_jumps_if_CFlag_is_not_set(self):
		ram = FakeRam([None]*0x3002)
		
		rom = FakeRom('\x00'*0x1A47+'\xD4\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = False
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram.readAddr(0x3001))
		self.assertEqual(0x4A, cpu.ram.readAddr(0x3000))

	def test_call_c_does_not_jumps_if_CFlag_is_set(self):
		ram = FakeRam([None]*0x3002)
		
		rom = FakeRom('\x00'*0x1A47+'\xD4\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = True
		cpu.readOp()

		self.assertEqual(0x1A49, cpu.PC)
		self.assertEqual(0x3002, cpu.SP)

	def test_call_po_jumps_if_PVFlag_is_not_set(self):
		ram = FakeRam([None]*0x3002)
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xe4\x35\x21'), ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = False
		cpu.readOp()
		self.assertEqual(0x2135, cpu.PC)

	def test_call_po_doesnt_jumps_if_PVFlag_is_set(self):
		ram = FakeRam([None]*0x3002)
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xe4\x35\x21'), ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(0x1A49, cpu.PC)
		self.assertEqual(0x3002, cpu.SP)

	def test_call_not_po_jumps_if_PVFlag_is_not_set(self):
		ram = FakeRam([None]*0x3002)
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xec\x20\x15'))
		cpu.PVFlag = False
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_call_s_jumps_if_SFlag_is_set(self):
		ram = FakeRam([None]*0x3002)
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xfc\x20\x15'))
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.SFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_call_not_s_jumps_if_SFlag_is_not_set(self):
		ram = FakeRam([None]*0x3002)
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xf4\x20\x15'))
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.SFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)
