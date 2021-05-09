import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_rlcn(unittest.TestCase):

    def test_rlcb_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x00'))
        cpu.B = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlcb_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x00'))
        cpu.B = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.B)

    def test_rlcc_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x01'))
        cpu.C = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlcc_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x01'))
        cpu.C = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.C)

    def test_rlcd_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x02'))
        cpu.D = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlcd_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x02'))
        cpu.D = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.D)

    def test_rlce_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x03'))
        cpu.E = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlce_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x03'))
        cpu.E = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.E)

    def test_rlch_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x04'))
        cpu.H = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlch_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x04'))
        cpu.H = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.H)

    def test_rlcl_sets_CF_correctly(self):
        cpu = CPU(ROM(b'\xcb\x05'))
        cpu.L = 0b10010001
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_rlcl_rotates_correctly(self):
        cpu = CPU(ROM(b'\xcb\x05'))
        cpu.L = 0b10001000
        cpu.readOp()
        self.assertEqual(0x11, cpu.L)

