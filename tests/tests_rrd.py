import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_rrd(unittest.TestCase):

    def test_rrd_does_modify_value_correctly(self):
        ram = RAM()
        ram[0x5000] = 0b00100000
        cpu = CPU(ROM(b'\xed\x67'), ram)
        cpu.A = 0b10000100
        cpu.HL = 0x5000
        cpu.readOp()
        self.assertEqual(0b10000000, cpu.A)
        self.assertEqual(0b01000010, cpu.ram[cpu.HL])

    def test_rrd_does_take_5_m_cycles(self):
        ram = RAM()
        ram[0x5000] = 0b00100000
        cpu = CPU(ROM(b'\xed\x67'), ram)
        cpu.A = 0b10000100
        cpu.HL = 0x5000
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_rrd_does_take_18_t_states(self):
        ram = RAM()
        ram[0x5000] = 0b00100000
        cpu = CPU(ROM(b'\xed\x67'), ram)
        cpu.A = 0b10000100
        cpu.HL = 0x5000
        cpu.readOp()
        self.assertEqual(18, cpu.t_states)
