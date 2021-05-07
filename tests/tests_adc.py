import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from rom import ROM
from utility import Bits


class tests_adc(unittest.TestCase):

    def test_add_HL_BC_with_C_flag_unset_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\xed\x4a'))
        cpu.HL = 0xCDCD
        cpu.BC = 0x1111
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0XCDCD+0x1111, cpu.HL)

    def test_add_HL_BC_with_C_flag_set_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\xed\x4a'))
        cpu.HL = 0xCDCD
        cpu.BC = 0x1111
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0XCDCD+0x1111+0x1, cpu.HL)

    def test_add_HL_DE_with_C_flag_set_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\xed\x5a'))
        cpu.HL = 0xCDCD
        cpu.DE = 0x1111
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0XCDCD+0x1111+0x1, cpu.HL)

    def test_add_HL_HL_with_C_flag_set_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\xed\x6a'))
        cpu.HL = 0x1111
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x1111+0x1111+0x1, cpu.HL)

    def test_add_HL_SP_with_C_flag_set_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\xed\x7a'))
        cpu.HL = 0x1111
        cpu.SP = 0x2222
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x1111+0x2222+0x1, cpu.HL)

    def test_add_a_b_with_C_flag_set_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\x88'))
        cpu.A = 0x12
        cpu.B = 0x12
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x25, cpu.A)

    def test_add_a_b_with_C_flag_reset_correctly_calculates_value(self):
        cpu = CPU(ROM(b'\x88'))
        cpu.A = 0x22
        cpu.B = 0x33
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x55, cpu.A)

    def test_add_a_c_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x89'))
        cpu.A = 0x22
        cpu.C = 0x88
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0xAB, cpu.A)

    def test_add_a_c_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x89'))
        cpu.A = 0x22
        cpu.C = 0x88
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0xAA, cpu.A)

    def test_add_a_d_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8a'))
        cpu.A = 0x22
        cpu.D = 0x77
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x9a, cpu.A)

    def test_add_a_d_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8a'))
        cpu.A = 0x22
        cpu.D = 0x77
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x99, cpu.A)

    def test_add_a_e_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8b'))
        cpu.A = 0x22
        cpu.E = 0x66
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x89, cpu.A)

    def test_add_a_e_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8b'))
        cpu.A = 0x22
        cpu.E = 0x66
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x88, cpu.A)

    def test_add_a_h_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8c'))
        cpu.A = 0x22
        cpu.H = 0x55
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x78, cpu.A)

    def test_add_a_h_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8c'))
        cpu.A = 0x22
        cpu.H = 0x55
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x77, cpu.A)

    def test_add_a_l_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8d'))
        cpu.A = 0x22
        cpu.L = 0x44
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x67, cpu.A)

    def test_add_a_l_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8d'))
        cpu.A = 0x22
        cpu.L = 0x44
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x66, cpu.A)

    def test_add_a_a_with_C_flag_set_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8f'))
        cpu.A = 0x22
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x45, cpu.A)

    def test_add_a_a_with_C_flag_reset_correctly_caluclates_value(self):
        cpu = CPU(ROM(b'\x8f'))
        cpu.A = 0x22
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x44, cpu.A)

    def test_add_a_a_with_C_flag_reset_correctly_sets_ZFlag(self):
        cpu = CPU(ROM(b'\x8f'))
        cpu.A = 0x00
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_add_a_a_with_C_flag_set_correctly_resets_ZFlag(self):
        cpu = CPU(ROM(b'\x8f'))
        cpu.A = 0x00
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_add_a_b_with_C_flag_set_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\x88'))
        cpu.A = 0x12
        cpu.B = 0x12
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_add_a_b_with_C_flag_set_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x88'))
        cpu.A = 0x12
        cpu.B = 0x12
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)

    def test_add_HL_BC_with_C_flag_unset_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\xed\x4a'))
        cpu.HL = 0xCDCD
        cpu.BC = 0x1111
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_add_HL_BC_with_C_flag_unset_takes_15_t_states(self):
        cpu = CPU(ROM(b'\xed\x4a'))
        cpu.HL = 0xCDCD
        cpu.BC = 0x1111
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(15, cpu.t_states)

    def test_adc_A_mem_HL_with_CFlag_reset_correctly_sets_A_register(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 0x5
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(12, cpu.A)

    def test_adc_A_mem_HL_with_CFlag_set_correctly_sets_A_register(self):
        cpu = CPU(ROM(b'\x8e\x15\x16\x17\x18'))
        cpu.HL = 0x03
        cpu.A = 0x5
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x1c, cpu.A)

    def test_adc_A_mem_HL_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 0x5
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_adc_A_mem_HL_takes_7_t_states(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 0x5
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_adc_A_mem_HL_sets_SFlag_when_result_is_negative(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 0x7f
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_adc_A_mem_HL_sets_ZFlag_when_result_is_zero(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 249
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_adc_A_mem_HL_sets_CFlag_when_result_is_over_byte(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 255
        cpu.readOp()
        self.assertTrue(cpu.CFlag)

    def test_adc_A_mem_HL_sets_HFlag_when_value_is_over_nibble(self):
        cpu = CPU(ROM(b'\x8e\x05\x06\x07\x08'))
        cpu.HL = 0x03
        cpu.A = 0x0F
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_adc_A_n_correctly_calculates_values(self):
        cpu = CPU(ROM(b'\xce\x02'))
        cpu.A = 0x02
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x05, cpu.A)
