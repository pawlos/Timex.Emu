import unittest
from cpu import CPU
from rom import ROM


class tests_djnz(unittest.TestCase):

    def test_djnz_doesn_jumps_if_B_is_zero_after_dec(self):
        cpu = CPU(ROM(b'\x10\x02'))
        cpu.B = 1
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(0x02, cpu.PC)

    def test_djnz_does_jumps_if_B_is_non_zero_after_dec(self):
        cpu = CPU(ROM(b'\x10\xFE'))
        cpu.B = 2
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(0x0, cpu.PC)

    def test_djnz_takes_3_m_cycles_if_B_is_non_zero(self):
        cpu = CPU(ROM(b'\x10\xFE'))
        cpu.B = 2
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_djnz_takes_13_t_states_if_B_is_non_zero(self):
        cpu = CPU(ROM(b'\x10\xFE'))
        cpu.B = 2
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(13, cpu.t_states)

    def test_djnz_takes_2_m_cycles_if_B_is_non_zero(self):
        cpu = CPU(ROM(b'\x10\xFE'))
        cpu.B = 1
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_djnz_takes_8_t_states_if_B_is_non_zero(self):
        cpu = CPU(ROM(b'\x10\xFE'))
        cpu.B = 1
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)
