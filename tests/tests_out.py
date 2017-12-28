import unittest
import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_out(unittest.TestCase):

	def test_out_to_port_0x22_puts_value_of_reg_A_to_port_0x22(self):
		cpu = CPU(FakeRom('\xd3\x22'), FakeRam())
		cpu.A = 0x33
		
		cpu.readOp()
		self.assertEqual(0x33, cpu.ports[0x22])