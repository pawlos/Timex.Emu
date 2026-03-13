import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_inc_ixh(unittest.TestCase):

    def test_inc_ixh_increments_high_byte(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xdd\x24'), ram)
        cpu.IX = 0x1000
        cpu.readOp()
        self.assertEqual(0x1100, cpu.IX)

    def test_inc_ixh_overflow_sets_pv_flag(self):
        # IXH = 0x7F -> 0x80: signed overflow, PV should be set
        ram = RAM()
        cpu = CPU(ROM(b'\xdd\x24'), ram)
        cpu.IX = 0x7F00
        cpu.readOp()
        self.assertEqual(0x8000, cpu.IX)
        self.assertTrue(cpu.PVFlag)

    def test_inc_ixh_sets_zero_flag(self):
        # IXH = 0xFF -> 0x00 (wraps): Z should be set
        ram = RAM()
        cpu = CPU(ROM(b'\xdd\x24'), ram)
        cpu.IX = 0xFF00
        cpu.readOp()
        self.assertEqual(0x0000, cpu.IX)
        self.assertTrue(cpu.ZFlag)

    def test_inc_ixh_sets_sign_flag(self):
        # IXH = 0x7F -> 0x80: S should be set (bit 7 = 1)
        ram = RAM()
        cpu = CPU(ROM(b'\xdd\x24'), ram)
        cpu.IX = 0x7F00
        cpu.readOp()
        self.assertTrue(cpu.SFlag)
