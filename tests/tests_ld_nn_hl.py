import unittest
from cpu import CPU
from rom import ROM


class tests_ld_nn_hl(unittest.TestCase):

    def test_ld_nn_hl_correctly_stores_value_at_given_address(self):
        cpu = CPU(ROM('\x22\xb2\x29'))
        cpu.HL = 0x483a
        cpu.readOp()
        self.assertEqual(0x48, cpu.ram[0xb22a])
        self.assertEqual(0x3a, cpu.ram[0xb229])

    def test_ld_nn_hl_does_not_affect_flags(self):
        cpu = CPU(ROM('\x22\xb2\x29'))
        cpu.HFlag = False
        cpu.ZFlag = True
        cpu.PVFlag = False
        cpu.SFlag = True

        self.assertFalse(cpu.HFlag)
        self.assertTrue(cpu.ZFlag)
        self.assertFalse(cpu.PVFlag)
        self.assertTrue(cpu.SFlag)

    def test_ld_nn_hl_takes_5_m_cycles(self):
        cpu = CPU(ROM('\x22\xb2\x29'))
        cpu.HL = 0x483a
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_nn_hl_takes_16_t_states(self):
        cpu = CPU(ROM('\x22\xb2\x29'))
        cpu.HL = 0x483a
        cpu.readOp()
        self.assertEqual(16, cpu.t_states)
