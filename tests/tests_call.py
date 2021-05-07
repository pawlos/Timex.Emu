import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_call(unittest.TestCase):

    def test_call(self):
        ram = RAM()

        rom = ROM(b'\x00'*0x1A47+b'\xcd\x35\x21')
        cpu = CPU(rom, ram)
        cpu.PC = 0x1A47
        cpu.SP = 0x3002
        cpu.readOp()

        self.assertEqual(0x2135, cpu.PC)
        self.assertEqual(0x1A, cpu.ram[0x3001])
        self.assertEqual(0x4A, cpu.ram[0x3000])

    def test_call_takes_5_m_cycles(self):
        ram = RAM()

        rom = ROM(b'\x00'*0x1A47+b'\xcd\x35\x21')
        cpu = CPU(rom, ram)
        cpu.PC = 0x1A47
        cpu.SP = 0x3002
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_call_Takes_17_t_states(self):
        ram = RAM()

        rom = ROM(b'\x00'*0x1A47+b'\xcd\x35\x21')
        cpu = CPU(rom, ram)
        cpu.PC = 0x1A47
        cpu.SP = 0x3002
        cpu.readOp()
        self.assertEqual(17, cpu.t_states)
