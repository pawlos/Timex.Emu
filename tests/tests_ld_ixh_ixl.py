import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_ld_ixh_ixl(unittest.TestCase):

    def test_ld_ixh_ixl_reads_ixl_not_l(self):
        # DD 65 = LD IXH, IXL
        cpu = CPU(ROM(b'\xdd\x65'))
        cpu.IX = 0xAB_CD
        cpu.L = 0x99
        cpu.readOp()
        # IXH should be set to IXL (0xCD), not L (0x99)
        self.assertEqual(0xCD, cpu.IX >> 8)
        self.assertEqual(0xCD, cpu.IX & 0xFF)

    def test_ld_ixl_ixl_is_noop(self):
        # DD 6D = LD IXL, IXL (should be no-op on IXL)
        cpu = CPU(ROM(b'\xdd\x6d'))
        cpu.IX = 0xAB_CD
        cpu.L = 0x99
        cpu.readOp()
        # IX should be unchanged
        self.assertEqual(0xABCD, cpu.IX)

    def test_ld_ixh_ixh_is_noop(self):
        # DD 64 = LD IXH, IXH (should be no-op on IXH)
        cpu = CPU(ROM(b'\xdd\x64'))
        cpu.IX = 0xAB_CD
        cpu.H = 0x99
        cpu.readOp()
        self.assertEqual(0xABCD, cpu.IX)

    def test_ld_iyh_iyl_reads_iyl_not_l(self):
        # FD 65 = LD IYH, IYL
        cpu = CPU(ROM(b'\xfd\x65'))
        cpu.IY = 0xAB_CD
        cpu.L = 0x99
        cpu.readOp()
        self.assertEqual(0xCD, cpu.IY >> 8)
        self.assertEqual(0xCD, cpu.IY & 0xFF)

    def test_ld_iyl_iyl_is_noop(self):
        # FD 6D = LD IYL, IYL (should be no-op on IYL)
        cpu = CPU(ROM(b'\xfd\x6d'))
        cpu.IY = 0xAB_CD
        cpu.L = 0x99
        cpu.readOp()
        self.assertEqual(0xABCD, cpu.IY)
