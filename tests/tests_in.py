import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_in(unittest.TestCase):

	def test_in_from_port_specified_in_c_puts_value_of_reg_A(self):
		cpu = CPU(FakeRom('\xed\x78'), FakeRam())
		cpu.C = 0x44
		cpu.io.writeTo(cpu.C, 0xAA)
		
		cpu.readOp()
		self.assertEqual(0xAA, cpu.io.readFrom(0x44))