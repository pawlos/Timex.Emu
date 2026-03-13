import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_ld_a_ixhl(unittest.TestCase):

    def test_ld_a_ixh_reads_from_ixh_not_h(self):
        # DD 7C = LD A, IXH
        cpu = CPU(ROM(b'\xdd\x7c'))
        cpu.IX = 0xAB00
        cpu.H = 0x99
        cpu.readOp()
        self.assertEqual(0xAB, cpu.A)

    def test_ld_a_ixl_reads_from_ixl_not_l(self):
        # DD 7D = LD A, IXL
        cpu = CPU(ROM(b'\xdd\x7d'))
        cpu.IX = 0x00CD
        cpu.L = 0x99
        cpu.readOp()
        self.assertEqual(0xCD, cpu.A)

    def test_ld_a_iyh_reads_from_iyh_not_h(self):
        # FD 7C = LD A, IYH
        cpu = CPU(ROM(b'\xfd\x7c'))
        cpu.IY = 0xEF00
        cpu.H = 0x99
        cpu.readOp()
        self.assertEqual(0xEF, cpu.A)

    def test_ld_a_iyl_reads_from_iyl_not_l(self):
        # FD 7D = LD A, IYL
        cpu = CPU(ROM(b'\xfd\x7d'))
        cpu.IY = 0x0012
        cpu.L = 0x99
        cpu.readOp()
        self.assertEqual(0x12, cpu.A)
