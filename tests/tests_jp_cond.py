import unittest
from cpu import CPU
from rom import ROM


class tests_jp_cond(unittest.TestCase):

    def test_jp_c_jumps_if_CFlag_is_set(self):
        cpu = CPU(ROM(b'\xDA\x20\x15'))
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_c_jumps_if_CFlag_is_not_set(self):
        cpu = CPU(ROM(b'\xD2\x20\x15'))
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_z_jumps_if_ZFlag_is_not_set(self):
        cpu = CPU(ROM(b'\xC2\x20\x15'))
        cpu.ZFlag = False
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_z_jumps_if_ZFlag_is_set(self):
        cpu = CPU(ROM(b'\xCA\x20\x15'))
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_po_jumps_if_PVFlag_is_not_set(self):
        cpu = CPU(ROM(b'\xe2\x20\x15'))
        cpu.PVFlag = False
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_po_jumps_if_PVFlag_is_set(self):
        cpu = CPU(ROM(b'\xea\x20\x15'))
        cpu.PVFlag = True
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_s_jumps_if_SFlag_is_not_set(self):
        cpu = CPU(ROM(b'\xF2\x20\x15'))
        cpu.SFlag = False
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_s_jumps_if_SFlag_is_set(self):
        cpu = CPU(ROM(b'\xFA\x20\x15'))
        cpu.SFlag = True
        cpu.readOp()
        self.assertEqual(0x1520, cpu.PC)

    def test_jp_s_takes_3_m_cycles(self):
        cpu = CPU(ROM(b'\xFA\x20\x15'))
        cpu.SFlag = True
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_jp_po_takes_10_t_states(self):
        cpu = CPU(ROM(b'\xea\x20\x15'))
        cpu.PVFlag = True
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)
