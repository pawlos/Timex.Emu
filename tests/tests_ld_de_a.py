import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class test_ld_de_a(unittest.TestCase):

    def test_ld_de_a_loads_corect_value(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x12'), ram)
        cpu.A = 0xA0
        cpu.DE = 0x1128
        cpu.readOp()
        self.assertEqual(0xA0, cpu.ram[cpu.DE])

    def test_ld_de_a_takes_2_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x12'), ram)
        cpu.A = 0xA0
        cpu.DE = 0x1128
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_de_a_takes_7_t_states(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x12'), ram)
        cpu.A = 0xA0
        cpu.DE = 0x1128
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)
