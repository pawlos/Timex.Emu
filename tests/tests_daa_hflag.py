import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_daa_hflag(unittest.TestCase):

    def test_daa_hflag_is_xor_of_old_and_new_bit4(self):
        # After SUB: A=0x13, NF=1, HF=1, CF=0
        # DAA subtracts 6: 0x13 - 0x06 = 0x0D
        # HF = (0x13 ^ 0x0D) bit 4 = 0x1E bit 4 = 1
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x13
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x0D, cpu.A)
        self.assertEqual(1, cpu.HFlag)

    def test_daa_hflag_cleared_when_xor_bit4_is_zero(self):
        # After SUB: A=0x06, NF=1, HF=1, CF=0
        # DAA subtracts 6: 0x06 - 0x06 = 0x00
        # HF = (0x06 ^ 0x00) bit 4 = 0x06 bit 4 = 0
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x06
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x00, cpu.A)
        self.assertEqual(0, cpu.HFlag)

    def test_daa_after_add_sets_hflag_when_low_nibble_wraps(self):
        # After ADD: A=0x0A, NF=0, HF=0, CF=0
        # DAA adds 6: 0x0A + 0x06 = 0x10
        # HF = (0x0A ^ 0x10) bit 4 = 0x1A bit 4 = 1
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x0A
        cpu.NFlag = Bits.reset()
        cpu.HFlag = Bits.reset()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x10, cpu.A)
        self.assertEqual(1, cpu.HFlag)
