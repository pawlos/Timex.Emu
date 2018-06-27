import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_push(unittest.TestCase):

	def test_push_correctly_stores_af_on_stack(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xF5'), ram)
		cpu.AF = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(0x22, ram.readAddr(0x1006))
		self.assertEqual(0x33, ram.readAddr(0x1005))

	def test_push_correctly_stores_hl_on_stack(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xE5'), ram)
		cpu.HL = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(0x22, ram.readAddr(0x1006))
		self.assertEqual(0x33, ram.readAddr(0x1005))

	def test_push_correctly_stores_bc_on_stack(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xC5'), ram)
		cpu.BC = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(0x22, ram.readAddr(0x1006))
		self.assertEqual(0x33, ram.readAddr(0x1005))

	def test_push_correctly_stores_de_on_stack(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xD5'), ram)
		cpu.DE = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(0x22, ram.readAddr(0x1006))
		self.assertEqual(0x33, ram.readAddr(0x1005))

	def test_push_takes_3_m_cycles(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xF5'), ram)
		cpu.AF = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_push_takes_11_t_states(self):
		ram = FakeRam([None]*0x1100)
		cpu = CPU(FakeRom('\xF5'), ram)
		cpu.AF = 0x2233
		cpu.SP = 0x1007
		
		cpu.readOp()
		self.assertEqual(11, cpu.t_states)	