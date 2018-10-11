import unittest
from cpu import CPU
from rom import ROM


class tests_ld_hl_addr(unittest.TestCase):
    def test_ld_hl_addr_correctly_stores_value_from_given_address_to_hl(self):
        cpu = CPU(ROM('\x2a\x45\x45'))
        cpu.ram[0x4545] = 0x37
        cpu.ram[0x4546] = 0xa1
        cpu.readOp()
        self.assertEqual(0xa137, cpu.HL)

    def test_ld_hl_does_not_affect_flags(self):
        cpu = CPU(ROM('\x2a\x45\x45'))
        cpu.ZFlag = True
        cpu.PVFlag = False
        cpu.HFlag = True
        cpu.NFlag = False
        cpu.SFlag = True
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)
        self.assertFalse(cpu.PVFlag)
        self.assertTrue(cpu.HFlag)
        self.assertFalse(cpu.NFlag)
        self.assertTrue(cpu.SFlag)

    def test_ld_hl_takes_5_m_cycles(self):
        cpu = CPU(ROM('\x2a\x45\x45'))
        cpu.ram[0x4545] = 0x37
        cpu.ram[0x4546] = 0xa1
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_hl_takes_16_t_states(self):
        cpu = CPU(ROM('\x2a\x45\x45'))
        cpu.ram[0x4545] = 0x37
        cpu.ram[0x4546] = 0xa1
        cpu.readOp()
        self.assertEqual(16, cpu.t_states)
