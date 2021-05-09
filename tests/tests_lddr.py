import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_lddr(unittest.TestCase):

    def test_lddr(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x03
        cpu.ram[0x1114] = 0xA5
        cpu.ram[0x1113] = 0x36
        cpu.ram[0x1112] = 0x88
        cpu.ram[0x2225] = 0xc5
        cpu.ram[0x2224] = 0x59
        cpu.ram[0x2223] = 0x66
        cpu.readOp()
        self.assertEqual(0x1111, cpu.HL)
        self.assertEqual(0x2222, cpu.DE)
        self.assertEqual(0x0000, cpu.BC)

        self.assertEqual(0xA5, cpu.ram[0x1114])
        self.assertEqual(0x36, cpu.ram[0x1113])
        self.assertEqual(0x88, cpu.ram[0x1112])

        self.assertEqual(0xA5, cpu.ram[0x2225])
        self.assertEqual(0x36, cpu.ram[0x2224])
        self.assertEqual(0x88, cpu.ram[0x2223])

    def test_lddr_does_set_flags_correctly(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x03
        cpu.HFlag = True
        cpu.NFlag = True
        cpu.PVFlag = True
        cpu.SFlag = False
        cpu.ZFlag = True
        cpu.ram[0x1114] = 0xA5
        cpu.ram[0x1113] = 0x36
        cpu.ram[0x1112] = 0x88
        cpu.ram[0x2225] = 0xc5
        cpu.ram[0x2224] = 0x59
        cpu.ram[0x2223] = 0x66
        cpu.readOp()
        self.assertFalse(cpu.HFlag)
        self.assertFalse(cpu.NFlag)
        self.assertFalse(cpu.PVFlag)
        self.assertFalse(cpu.SFlag)
        self.assertTrue(cpu.ZFlag)

    def test_lddr_when_bc_not_zero_takes_5_m_cycles(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x03
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_lddr_when_bc_is_zero_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x0
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_lddr_when_bc_not_zero_takes_21_t_states(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x03
        cpu.readOp()
        self.assertEqual(21, cpu.t_states)

    def test_lddr_when_bc_is_zero_takes_16_t_states(self):
        cpu = CPU(ROM(b'\xed\xb8'))
        cpu.HL = 0x1114
        cpu.DE = 0x2225
        cpu.BC = 0x0
        cpu.readOp()
        self.assertEqual(16, cpu.t_states)
