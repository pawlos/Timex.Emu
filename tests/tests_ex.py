import unittest
from cpu import CPU
from rom import ROM


class tests_ex(unittest.TestCase):
    def test_ex_de_hl_exchanges_16_bit_hl_de_registers(self):
        cpu = CPU(ROM(b'\xeb'))
        cpu.HL = 0xabba
        cpu.DE = 0xc0de
        cpu.readOp()
        self.assertEqual(0xc0de, cpu.HL)
        self.assertEqual(0xabba, cpu.DE)

    def test_ex_de_hl_takes_1_m_cycle(self):
        cpu = CPU(ROM(b'\xeb'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ex_de_hl_takes_4_t_states(self):
        cpu = CPU(ROM(b'\xeb'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)

    def test_ex_af_afprim_exchanges_correctly(self):
        cpu = CPU(ROM(b'\x08'))
        cpu.AF = 0x11
        cpu.AFPrim = 0x22
        cpu.readOp()
        self.assertEqual(0x22, cpu.AF)
        self.assertEqual(0x11, cpu.AFPrim)

    def test_ex_af_afprim_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\x08'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ex_af_afprim_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x08'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
