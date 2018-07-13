import unittest
from cpu import CPU
from ram import RAM
from opcodes import Opcodes
from rom import ROM
from loggers import Logger

class tests_rld(unittest.TestCase):

	def test_rld_does_modify_value_correctly(self):
		ram = RAM()
		ram[0x5000] = 0b00110001
		cpu = CPU(ROM('\xed\x6f'), ram)
		cpu.A = 0b01111010
		cpu.HL = 0x5000
		cpu.readOp()
		self.assertEqual(0b01110011, cpu.A)
		self.assertEqual(0b00011010, cpu.ram[cpu.HL])

	def test_rld_takes_5_m_cycles(self):
		ram = RAM()
		ram[0x5000] = 0b00110001
		cpu = CPU(ROM('\xed\x6f'), ram)
		cpu.A = 0b01111010
		cpu.HL = 0x5000
		cpu.readOp()
		self.assertEqual(5, cpu.m_cycles)

	def test_rld_takes_18_t_states(self):
		ram = RAM()
		ram[0x5000] = 0b00110001
		cpu = CPU(ROM('\xed\x6f'), ram)
		cpu.A = 0b01111010
		cpu.HL = 0x5000
		cpu.readOp()
		self.assertEqual(18, cpu.t_states)