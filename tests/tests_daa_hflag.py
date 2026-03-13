import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_daa_hflag(unittest.TestCase):

    def test_daa_after_sub_clears_hflag_when_low_nibble_ge_6(self):
        # After SUB: A=0x13, NF=1, HF=1, CF=0
        # DAA should subtract 6 from low nibble: 0x13 - 0x06 = 0x0D
        # HF after DAA (subtraction): HF_before AND (result & 0xF) < 6
        # HF_before=1, result_low=0xD, 0xD < 6 is False => HF should be 0
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x13
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x0D, cpu.A)
        self.assertEqual(0, cpu.HFlag)

    def test_daa_after_sub_keeps_hflag_when_low_nibble_lt_6(self):
        # After SUB: A=0x10, NF=1, HF=1, CF=0
        # DAA should subtract 6: 0x10 - 0x06 = 0x0A
        # HF after DAA: HF_before=1, (0x0A & 0xF)=0xA, 0xA < 6 False => HF=0
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x10
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x0A, cpu.A)
        self.assertEqual(0, cpu.HFlag)

    def test_daa_after_sub_with_low_result(self):
        # After SUB: A=0x06, NF=1, HF=1, CF=0
        # DAA: subtract 6: 0x06 - 0x06 = 0x00
        # HF: HF_before=1, (0x00 & 0xF)=0, 0 < 6 True => HF=1
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0x06
        cpu.NFlag = Bits.set()
        cpu.HFlag = Bits.set()
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x00, cpu.A)
        self.assertEqual(1, cpu.HFlag)
