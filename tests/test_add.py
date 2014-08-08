import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestAdd(unittest.TestCase):

	def test_add_hl_de_returns_correct_result(self):
		cpu = CPU(FakeRom('\x19'))
		cpu.HL = 0xa00a
		cpu.DE = 0x0bb0
		cpu.readOp()
		self.assertEqual(0xabba, cpu.HL)
