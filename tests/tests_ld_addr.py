import tests_suite

import unittest
from cpu import CPU
from rom import ROM
from ram import RAM


class test_ld_addr(unittest.TestCase):

    def test_ld_addr_hl_does_set_value_in_address_pointed_by_HL(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x36\x22'), ram)
        cpu.HL = 0x2222
        cpu.readOp()
        self.assertEqual(0x22, ram[0x2222])

    def test_ld_addr_hl_takes_3_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x36\x22'), ram)
        cpu.HL = 0x2222
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_ld_addr_hl_takes_10_t_states(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x36\x22'), ram)
        cpu.HL = 0x2222
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)