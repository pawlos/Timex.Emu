import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ccf(unittest.TestCase):

	def test_ccf_inverts_c(self):
		cpu = CPU(FakeRom('\x3f'), FakeRam())
		cpu.CFlag = True
		cpu.readOp();
		self.assertFalse(cpu.CFlag)

