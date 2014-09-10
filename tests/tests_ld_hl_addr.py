import unittest

from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class ld_hl_addr(unittest.TestCase):

	def test_ld_hl_addr_correctly_stores_value_from_given_address_to_hl(self):
		cpu = CPU(FakeRom('\x2a\x45\x45'))
		cpu.ram.storeAddr(0x4545, 0x37)
		cpu.ram.storeAddr(0x4546, 0xa1)
		cpu.readOp()
		self.assertEqual(0xa137, cpu.HL)