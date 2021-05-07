import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_bc_a(unittest.TestCase):

    def test_ld_bc_a_loads_corect_value(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x02'), ram)
        cpu.A = 0x7a
        cpu.BC = 0x1212
        cpu.readOp()
        self.assertEqual(0x7a, cpu.ram[cpu.BC])
