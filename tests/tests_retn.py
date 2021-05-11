import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_retn(unittest.TestCase):

    def test_retn_0xed45_does_sets_PC_correctly(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x45'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)


    def test_retn_0xed55_does_sets_PC_correctly(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x55'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)


    def test_retn_0xed65_does_sets_PC_correctly(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x65'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_retn_0xed75_does_sets_PC_correctly(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xed\x75'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)
