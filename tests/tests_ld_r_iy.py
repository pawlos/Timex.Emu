import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_r_iy(unittest.TestCase):

    def test_ld_a_iy_correctly_copies_value_to_a(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x7e\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.A)

    def test_ld_b_iy_correctly_copies_value_to_b(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x46\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.B)

    def test_ld_c_iy_correctly_copies_value_to_c(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x4e\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.C)

    def test_ld_d_iy_correctly_copies_value_to_d(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x56\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.D)

    def test_ld_e_iy_correctly_copies_value_to_e(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x5e\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.E)

    def test_ld_h_iy_correctly_copies_value_to_h(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x66\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.H)

    def test_ld_l_iy_correctly_copies_value_to_l(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x6e\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(0x39, cpu.L)

    def test_ld_b_iy_takes_5_m_cycles(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x46\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_ld_b_iy_takes_19_t_states(self):
        ram = RAM()
        ram[0x25af+0x19] = 0x39
        cpu = CPU(ROM('\xFD\x46\x19'), ram)
        cpu.IY = 0x25AF
        cpu.readOp()
        self.assertEqual(19, cpu.t_states)
