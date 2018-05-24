import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_pop(unittest.TestCase):

	def test_pop_correctly_retreives_value_from_stack(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xe1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.HL)


	def test_pop_bc_correctly_retreives_value_from_stack(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xc1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.BC)
	
	def test_pop_de_correctly_retreives_value_from_stack(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xd1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.DE)

	def test_pop_af_correctly_retreives_value_from_stack(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xf1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(0x3355, cpu.AF)

	def test_pop_bc_takes_3_m_cycles(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xc1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(3, cpu.m_cycles)

	def test_pop_bc_takes_7_t_states(self):
		ram = FakeRam([None]*0x1100)
		ram.storeAddr(0x1000, 0x55)
		ram.storeAddr(0x1001, 0x33)
		cpu = CPU(FakeRom('\xc1'), ram)
		cpu.SP = 0x1000
		
		cpu.readOp()
		self.assertEqual(7, cpu.t_states)