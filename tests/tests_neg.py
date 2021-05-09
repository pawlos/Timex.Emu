import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_neg(unittest.TestCase):

    def test_neg_does_negate_the_value(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10011000
        cpu.readOp()
        self.assertEqual(0b01101000, cpu.A)

    def test_neg_does_reset_nflag(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10011000
        cpu.NFlag = True
        cpu.readOp()
        self.assertFalse(cpu.NFlag)

    def test_neg_does_reset_zflag_if_result_is_not_zero(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10011000
        cpu.ZFlag = True
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_neg_does_set_zflag_if_result_is_zero(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.ZFlag = False
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_neg_does_set_sflag_if_result_is_negative(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00011000
        cpu.SFlag = False
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_neg_does_reset_sflag_if_result_is_not_negative(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.SFlag = True
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_neg_does_set_pvflag_if_A_was_80h(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10000000
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)

    def test_neg_does_reset_pvflag_if_A_was_not_80h(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10000001
        cpu.PVFlag = True
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)

    def test_neg_does_set_cflag_if_A_was_0h(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.CFlag = False
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_neg_does_reset_cflag_if_A_was_not_0h(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b10000001
        cpu.CFlag = True
        cpu.readOp()
        self.assertFalse(cpu.CFlag)

    def test_neg_does_set_hflag_if_there_was_a_borrow_on_4th_bit(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00011000
        cpu.HFlag = False
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_neg_does_reset_hflag_if_there_was_no_borrow_on_4th_bit(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.HFlag = True
        cpu.readOp()
        self.assertFalse(cpu.HFlag)

    def test_neg_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_neg_takes_8_t_states(self):
        cpu = CPU(ROM(b'\xed\x44'))
        cpu.A = 0b00000000
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)
