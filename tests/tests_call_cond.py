import unittest

from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from fakes import *
from loggers import Logger
from utility import Bits

class tests_call_cond(unittest.TestCase):

	def test_call_c_jumps_if_CFlag_is_not_set(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xD4\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = False
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram[0x3001])
		self.assertEqual(0x4A, cpu.ram[0x3000])

	def test_call_c_does_not_jumps_if_CFlag_is_set(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xD4\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = True
		cpu.readOp()

		self.assertEqual(0x1A49, cpu.PC)
		self.assertEqual(0x3002, cpu.SP)

	def test_call_po_jumps_if_PVFlag_is_not_set(self):
		ram = RAM()
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xe4\x35\x21'), ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = False
		cpu.readOp()
		self.assertEqual(0x2135, cpu.PC)

	def test_call_po_doesnt_jumps_if_PVFlag_is_set(self):
		ram = RAM()
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xe4\x35\x21'), ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(0x1A49, cpu.PC)
		self.assertEqual(0x3002, cpu.SP)

	def test_call_not_po_jumps_if_PVFlag_is_not_set(self):
		ram = RAM()
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xec\x20\x15'))
		cpu.PVFlag = False
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		
		cpu.PVFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_call_s_jumps_if_SFlag_is_set(self):
		ram = RAM()
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xfc\x20\x15'))
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.SFlag = True
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_call_not_s_jumps_if_SFlag_is_not_set(self):
		ram = RAM()
		cpu = CPU(FakeRom('\x00'*0x1A47+'\xf4\x20\x15'))
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.SFlag = False
		cpu.readOp()
		self.assertEqual(0x1520, cpu.PC)

	def test_call_nz_jumps_if_ZFlag_is_not_set(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xC4\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.ZFlag = False
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram[0x3001])
		self.assertEqual(0x4A, cpu.ram[0x3000])

	def test_call_z_jumps_if_ZFlag_is_set(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xCC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.ZFlag = True
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram[0x3001])
		self.assertEqual(0x4A, cpu.ram[0x3000])

	def test_call_c_jumps_if_CFlag_is_set(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xDC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = True
		cpu.readOp()

		self.assertEqual(0x2135, cpu.PC)
		self.assertEqual(0x1A, cpu.ram[0x3001])
		self.assertEqual(0x4A, cpu.ram[0x3000])


	def test_call_cc_takes_5_m_cycles_if_condition_is_true(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xDC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = Bits.set()
		cpu.readOp()

		self.assertEqual(5, cpu.m_cycles)

	def test_call_cc_takes_3_m_cycles_if_condition_is_false(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xDC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = Bits.reset()
		cpu.readOp()

		self.assertEqual(3, cpu.m_cycles)

	def test_call_cc_takes_17_t_states_if_condition_is_true(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xDC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = Bits.set()
		cpu.readOp()

		self.assertEqual(17, cpu.t_states)

	def test_call_cc_takes_10_t_cycles_if_condition_is_false(self):
		ram = RAM()
		
		rom = FakeRom('\x00'*0x1A47+'\xDC\x35\x21')
		cpu = CPU(rom, ram)
		cpu.PC = 0x1A47
		cpu.SP = 0x3002
		cpu.CFlag = Bits.reset()
		cpu.readOp()

		self.assertEqual(10, cpu.t_states)
