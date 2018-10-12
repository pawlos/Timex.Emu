import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_a_bc(unittest.TestCase):

    def test_ld_a_bc_loads_corect_value(self):
        ram = RAM()
        ram[0x4747] = 0x12
        cpu = CPU(ROM('\x0a'), ram)
        cpu.BC = 0x4747
        cpu.readOp()
        self.assertEqual(0x12, cpu.A)

    def test_ld_a_bc_takes_2_m_cycles(self):
        ram = RAM()
        ram[0x4747] = 0x12
        cpu = CPU(ROM('\x0a'), ram)
        cpu.BC = 0x4747
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_a_bc_takes_7_t_states(self):
        ram = RAM()
        ram[0x4747] = 0x12
        cpu = CPU(ROM('\x0a'), ram)
        cpu.BC = 0x4747
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)
