import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_r_ix(unittest.TestCase):

    def test_ld_c_ixh_correctly_copies_value_to_a(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x4c'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x25, cpu.C)

    def test_ld_b_ixh_correctly_copies_value_to_b(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x44'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x25, cpu.B)

    def test_ld_c_ixh_correctly_copies_value_to_c(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x4e'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.C)

    def test_ld_d_ix_correctly_copies_value_to_d(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x56'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.D)

    def test_ld_e_ix_correctly_copies_value_to_e(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x5e'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.E)

    def test_ld_h_ix_correctly_copies_value_to_h(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x66'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.H)

    def test_ld_l_ix_correctly_copies_value_to_l(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x6e'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.L)

    def test_ld_x_ixh_takes_1_m_cycles(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x44'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ld_x_ixh_takes_4_t_states(self):
        ram = RAM()
        ram[0x25AF] = 0x39
        cpu = CPU(ROM(b'\xDD\x44'), ram)
        cpu.IX = 0x25AF
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)
