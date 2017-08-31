import unittest
from cpu import CPU
from opcodes import Opcodes
from fakes import *
from loggers import Logger

class TestSBC(unittest.TestCase):

	def test_dec_mem_iy_result_doesnt_affect_c_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.CFlag = True
		cpu.readOp();
		self.assertEqual(True, cpu.CFlag)

	def test_dec_mem_iy_result_is_decreased_by_one(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.readOp();
		self.assertEqual(0x00, ram.readAddr(0x00))

	def test_dec_mem_iy_sets_n_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.NFlag = False
		cpu.readOp()
		self.assertTrue(cpu.NFlag)

	def test_dec_mem_iy_that_results_zero_sets_z_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.ZFlag = False
		cpu.readOp()
		self.assertTrue(cpu.ZFlag)

	def test_dec_mem_iy_that_results_non_zero_resets_z_flag(self):
		ram = FakeRam([0x02])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.CFlag = True
		cpu.ZFlag = True
		cpu.readOp()
		self.assertFalse(cpu.ZFlag)

	def test_dec_mem_iy_that_results_in_borrow_sets_h_flag(self):
		ram = FakeRam([0x00])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.CFlag = True
		cpu.HFlag = False
		cpu.readOp()
		self.assertTrue(cpu.HFlag)

	def test_dec_mem_iy_that_does_not_generate_carry_on_12bit_resets_h_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.HFlag = True
		cpu.readOp()
		self.assertFalse(cpu.HFlag)


	def test_dec_mem_iy_that_results_in_value_less_than_zero_set_s_flag(self):
		ram = FakeRam([0x00])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.SFLag = False
		cpu.readOp()
		self.assertTrue(cpu.SFlag)

	def test_dec_mem_iy_that_results_in_value_greater_than_zero_resets_s_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.SFLag = True
		cpu.readOp()
		self.assertFalse(cpu.SFlag)

	def test_dec_mem_iy_that_overflows_sets_pv_flag(self):
		ram = FakeRam([0x80])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.PVFlag = False
		cpu.readOp()
		self.assertTrue(cpu.PVFlag)

	def test_dec_mem_iy_that_does_not_overflows_resets_pv_flag(self):
		ram = FakeRam([0x01])
		cpu = CPU(FakeRom('\xfd\x35\x00'), ram)
		cpu.IY = 0x0
		cpu.PVFlag = True
		cpu.readOp()
		self.assertFalse(cpu.PVFlag)