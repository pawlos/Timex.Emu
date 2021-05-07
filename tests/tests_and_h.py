import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from rom import ROM


class tests_and_h(unittest.TestCase):
    def test_and_h_that_returns_0_set_z_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x10
        cpu.A = 0x01
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_and_h_that_returns_non_0_reset_z_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x11
        cpu.A = 0x10
        cpu.ZFlag = True
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_and_h_that_returns_negative_set_s_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x88
        cpu.A = 0x81
        cpu.SFlag = False
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_and_h_that_returns_positive_resets_s_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x88
        cpu.A = 0x08
        cpu.SFlag = True
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_and_h_that_results_with_even_no_of_ones_sets_pv_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x89
        cpu.A = 0x09
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)

    def test_and_h_that_results_with_odd_no_of_ones_resets_pv_flag(self):
        cpu = CPU(ROM(b'\xa4'))
        cpu.H = 0x80
        cpu.A = 0x09
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)
