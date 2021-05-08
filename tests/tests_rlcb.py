import unittest
from cpu import CPU
from rom import ROM


class tests_rlcb(unittest.TestCase):

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

