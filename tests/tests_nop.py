import unittest
from cpu import CPU
from rom import ROM


class tests_nop(unittest.TestCase):

    def test_nop_does_not_change_hl(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.HL = 0x9999
        cpu.readOp()
        self.assertEqual(0x9999, cpu.HL)

    def test_nop_does_not_change_de(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.DE = 0x8999
        cpu.readOp()
        self.assertEqual(0x8999, cpu.DE)

    def test_nop_does_not_change_bc(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.BC = 0x1223
        cpu.readOp()
        self.assertEqual(0x1223, cpu.BC)

    def test_nop_does_not_change_sp(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.SP = 0x9799
        cpu.readOp()
        self.assertEqual(0x9799, cpu.SP)

    def test_nop_does_not_change_a(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.A = 0x99
        cpu.readOp()
        self.assertEqual(0x99, cpu.A)

    def test_2_nops_takes_2_m_cycles(self):
        cpu = CPU(ROM(b'\x00\x00'))
        cpu.readOp()
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_2_nop_takes_8_t_states(self):
        cpu = CPU(ROM(b'\x00\x00'))
        cpu.readOp()
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)

    def test_nop_takes_1_m_cycles(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_nop_takes_4_t_states(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
