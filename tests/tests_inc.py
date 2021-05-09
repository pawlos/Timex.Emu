import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_inc(unittest.TestCase):
    def test_inc_hl_does_add_1_to_hl_value(self):
        cpu = CPU(ROM(b'\x23'))
        cpu.HL = 0xfff
        cpu.readOp()
        self.assertEqual(0x1000, cpu.HL)

    def test_inc_bc_does_add_1_to_bc_value(self):
        cpu = CPU(ROM(b'\x03'))
        cpu.BC = 0xfff
        cpu.readOp()
        self.assertEqual(0x1000, cpu.BC)

    def test_inc_de_does_add_1_to_de_value(self):
        cpu = CPU(ROM(b'\x13'))
        cpu.DE = 0xfff
        cpu.readOp()
        self.assertEqual(0x1000, cpu.DE)

    def test_inc_sp_does_add_1_to_sp_value(self):
        cpu = CPU(ROM(b'\x33'))
        cpu.SP = 0xfff
        cpu.readOp()
        self.assertEqual(0x1000, cpu.SP)

    def test_inc_hl_does_not_affect_c_flag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xfff
        cpu.CFlag = True
        cpu.readOp()
        self.assertTrue(cpu.CFlag)
        cpu.CFlag = False
        cpu.readOp()
        self.assertFalse(cpu.CFlag)

    def test_inc_hl_does_not_affect_z_flag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xffff
        cpu.ZFlag = True
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)
        cpu.ZFlag = False
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_inc_hl_does_not_affect_pv_flag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xfff
        cpu.PVFlag = True
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)
        cpu.PVFlag = False
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)

    def test_inc_hl_does_not_affect_n_hlag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xfff
        cpu.NFlag = True
        cpu.readOp()
        self.assertTrue(cpu.NFlag)
        cpu.NFlag = False
        cpu.readOp()
        self.assertFalse(cpu.NFlag)

    def test_inc_hl_does_not_affect_s_hlag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xfff
        cpu.SFlag = True
        cpu.readOp()
        self.assertTrue(cpu.SFlag)
        cpu.SFlag = False
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_inc_hl_does_not_affect_h_hlag(self):
        cpu = CPU(ROM(b'\x23\x23'))
        cpu.HL = 0xfff
        cpu.HFlag = True
        cpu.readOp()
        self.assertTrue(cpu.HFlag)
        cpu.HFlag = False
        cpu.readOp()
        self.assertFalse(cpu.HFlag)

    def test_inc_B_correctly_adds_one(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0
        cpu.readOp()
        self.assertEqual(1, cpu.B)

    def test_inc_C_correctly_adds_one(self):
        cpu = CPU(ROM(b'\x0c'))
        cpu.C = 0
        cpu.readOp()
        self.assertEqual(1, cpu.C)

    def test_inc_r_does_reset_N_flag(self):
        cpu = CPU(ROM(b'\x04\x04'))
        cpu.B = 0xAA
        cpu.NFlag = True
        cpu.readOp()
        self.assertFalse(cpu.NFlag)
        cpu.NFlag = False
        cpu.readOp()
        self.assertFalse(cpu.NFlag)

    def test_inc_r_does_not_affect_C_flag(self):
        cpu = CPU(ROM(b'\x04\x04'))
        cpu.B = 0xCB
        cpu.CFlag = True
        cpu.readOp()
        self.assertTrue(cpu.CFlag)
        cpu.readOp()
        cpu.CFlag = False
        self.assertFalse(cpu.CFlag)

    def test_inc_r_does_reset_Z_flag_when_result_is_non_zero(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0
        cpu.ZFlag = True
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_inc_r_set_Z_flag_when_result_is_zero(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0xff
        cpu.ZFlag = False
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_inc_r_set_H_flag_if_bit_no_3_is_set(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0x07
        cpu.HFlag = False
        cpu.readOp()
        self.assertTrue(cpu.HFlag)

    def test_inc_r_reset_H_flag_if_bit_no_3_is_reset(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0x0f
        cpu.HFlag = True
        cpu.readOp()
        self.assertFalse(cpu.HFlag)

    def test_inc_r_sets_PV_flag_if_value_before_was_7f(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0x7f
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)

    def test_inc_r_resets_PV_flag_when_value_before_was_not_7f(self):
        cpu = CPU(ROM(b'\x04\x04'))
        cpu.B = 0x7e
        cpu.PVFlag = True
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)
        cpu.B = 0x80
        cpu.PVFlag = True
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)

    def test_inc_r_sets_S_flag_when_result_is_negative(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0x7f
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_inc_r_resets_S_flag_when_result_is_positive(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.B = 0x11
        cpu.SFlag = True
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_inc_r_increases_h_when_opcode_is_24(self):
        cpu = CPU(ROM(b'\x24'))
        cpu.H = 0x11
        cpu.readOp()
        self.assertEqual(0x12,cpu.H)

    def test_inc_r_increases_l_when_opcode_is_2c(self):
        cpu = CPU(ROM(b'\x2c'))
        cpu.L = 0x99
        cpu.readOp()
        self.assertEqual(0x9a, cpu.L)

    def test_inc_r_increases_a_when_opcode_is_3c(self):
        cpu = CPU(ROM(b'\x3c'))
        cpu.A = 0x10
        cpu.readOp()
        self.assertEqual(0x11, cpu.A)

    def test_inc_e_does_add_1_to_e_value(self):
        cpu = CPU(ROM(b'\x1c'))
        cpu.E = 0xf
        cpu.readOp()
        self.assertEqual(0x10, cpu.E)

    def test_inc_bc_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\x03'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_inc_bc_takes_6_t_states(self):
        cpu = CPU(ROM(b'\x03'))
        cpu.readOp()
        self.assertEqual(6, cpu.t_states)

    def test_inc_b_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_inc_b_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x04'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
