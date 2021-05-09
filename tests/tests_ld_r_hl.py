import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_r_hl(unittest.TestCase):

    def test_ld_b_hl_correctly_copies_value_to_b(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x46'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.B)

    def test_ld_c_hl_correctly_copies_value_to_c(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x4e'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.C)

    def test_ld_d_hl_correctly_copies_value_to_d(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x56'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.D)

    def test_ld_e_hl_correctly_copies_value_to_e(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x5e'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.E)

    def test_ld_h_hl_correctly_copies_value_to_h(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x66'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.H)

    def test_ld_l_hl_correctly_copies_value_to_l(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x6e'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.L)

    def test_ld_a_hl_correctly_copies_value_to_a(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x7e'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.A)

    def test_ld_b_hl_takes_2_m_cycles(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x46'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_b_hl_takes_7_t_states(self):
        ram = RAM()
        ram[0x25af] = 0x39
        cpu = CPU(ROM(b'\x46'), ram)
        cpu.HL = 0x25AF
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)
