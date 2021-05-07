import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_a_nn(unittest.TestCase):

    def test_ld_a_nn_loads_corect_value(self):
        ram = RAM()
        ram[0x8832] = 0x04
        cpu = CPU(ROM(b'\x3a\x32\x88'), ram)
        cpu.readOp()
        self.assertEqual(0x4, cpu.A)

    def test_ld_a_nn_takes_4_m_cycles(self):
        ram = RAM()
        ram[0x8832] = 0x04
        cpu = CPU(ROM(b'\x3a\x32\x88'), ram)
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_ld_a_nn_takes_13_t_states(self):
        ram = RAM()
        ram[0x8832] = 0x04
        cpu = CPU(ROM(b'\x3a\x32\x88'), ram)
        cpu.readOp()
        self.assertEqual(13, cpu.t_states)
