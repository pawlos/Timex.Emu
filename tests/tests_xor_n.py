import unittest
from cpu import CPU
from rom import ROM


class tests_xor_n(unittest.TestCase):
    def test_xor_n_works_correctly(self):
        cpu = CPU(ROM(b'\xee\x20'))
        cpu.A = 12
        cpu.readOp()
        self.assertEqual(44, cpu.A)

    def test_xor_n_sets_ZFlag_when_result_is_zero(self):
        cpu = CPU(ROM(b'\xee\x12'))
        cpu.A = 0x12
        cpu.readOp()
        self.assertEqual(0, cpu.A)
        self.assertTrue(cpu.ZFlag)

    def test_xor_n_resets_ZFlag_when_result_is_not_zero(self):
        cpu = CPU(ROM(b'\xee\x13'))
        cpu.A = 0x12
        cpu.ZFlag = True
        cpu.readOp()
        self.assertNotEqual(0, cpu.A)
        self.assertFalse(cpu.ZFlag)

    def test_xor_n_resets_CFlag(self):
        cpu = CPU(ROM(b'\xee\x13'))
        cpu.A = 0x12
        cpu.CFlag = True
        cpu.readOp()
        self.assertFalse(cpu.CFlag)

    def test_xor_n_resets_NFlag(self):
        cpu = CPU(ROM(b'\xee\x13'))
        cpu.A = 0x12
        cpu.NFlag = True
        cpu.readOp()
        self.assertFalse(cpu.NFlag)

    def test_xor_n_resets_HFlag(self):
        cpu = CPU(ROM(b'\xee\x00'))
        cpu.A = 0x12
        cpu.HFlag = True
        cpu.readOp()
        self.assertFalse(cpu.HFlag)

    def test_xor_n_sets_SFlag_when_result_is_negative(self):
        cpu = CPU(ROM(b'\xee\x96'))
        cpu.A = 0x5D
        cpu.SFlag = False
        cpu.readOp()
        self.assertTrue(cpu.SFlag)

    def test_xor_n_resets_SFlag_when_result_is_positive(self):
        cpu = CPU(ROM(b'\xee\x55'))
        cpu.A = 0x12
        cpu.SFlag = True
        cpu.readOp()
        self.assertFalse(cpu.SFlag)

    def test_xor_n_sets_PVFlag_when_parity_is_even(self):
        cpu = CPU(ROM(b'\xee\x11'))
        cpu.A = 0x44
        cpu.PVFlag = False
        cpu.readOp()
        self.assertTrue(cpu.PVFlag)

    def test_xor_n_resets_PVFlag_when_parity_is_odd(self):
        cpu = CPU(ROM(b'\xee\x11'))
        cpu.A = 0x45
        cpu.PVFlag = True
        cpu.readOp()
        self.assertFalse(cpu.PVFlag)

    def test_xor_a_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\xee\x11'))
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_xor_a_takes_7_t_states(self):
        cpu = CPU(ROM(b'\xee\x08'))
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)
