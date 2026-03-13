import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_retn_timing(unittest.TestCase):

    def test_retn_takes_4_m_cycles(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x45'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_retn_takes_14_t_states(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x45'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(14, cpu.t_states)
