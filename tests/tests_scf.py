import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class tests_ccf(unittest.TestCase):

	def test_scf_inverts_c(self):
		cpu = CPU(FakeRom('\x37'), FakeRam())
		cpu.CFlag = False
		cpu.readOp();
		self.assertTrue(cpu.CFlag)

