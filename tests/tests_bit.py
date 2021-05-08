import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_bit(unittest.TestCase):

    def test_bit_IY_plus_4_set_correctly_set_z_flag(self):
        ram = RAM()
        ram[0x2004] = 1 << 6
        cpu = CPU(ROM(b'\xfd\xcb\x04\x76'), ram)
        cpu.ZFlag = Bits.reset()
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_bit_IY_plus_1_set_correctly_the_value(self):
        ram = RAM()
        ram[0x2001] = 0b00001101
        cpu = CPU(ROM(b'\xfd\xcb\x01\xce'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(0x0F, ram[0x2001])

    def test_bit_IY_plus_30_reset_correctly_bit(self):
        ram = RAM()
        ram[0x2030] = 0b00001111
        cpu = CPU(ROM(b'\xfd\xcb\x30\x8e'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(0b1101, ram[0x2030])

    def test_bit_plus_x_takes_6_m_cycles(self):
        ram = RAM()
        ram[0x2001] = 0b00001111
        cpu = CPU(ROM(b'\xfd\xcb\x01\xce'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(6, cpu.m_cycles)

    def test_bit_plus_x_takes_20_t_states(self):
        ram = RAM()
        ram[0x2001] = 0b00001111
        cpu = CPU(ROM(b'\xfd\xcb\x01\xce'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(23, cpu.t_states)

    def test_bit_IY_plus_30_takes_6_m_cycles(self):
        ram = RAM()
        ram[0x2030] = 0b00001111
        cpu = CPU(ROM(b'\xfd\xcb\x30\x8e'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(6, cpu.m_cycles)

    def test_bit_IY_plus_30_takes_23_t_states(self):
        ram = RAM()
        ram[0x2030] = 0b00001111
        cpu = CPU(ROM(b'\xfd\xcb\x30\x8e'), ram)
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(23, cpu.t_states)

    def test_bit_IY_plus_4_takes_5_m_cycles(self):
        ram = RAM()
        ram[0x2004] = 1 << 6
        cpu = CPU(ROM(b'\xfd\xcb\x04\x76'), ram)
        cpu.ZFlag = Bits.reset()
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(5, cpu.m_cycles)

    def test_bit_IY_plus_4_takes_20_t_states(self):
        ram = RAM()
        ram[0x2004] = 1 << 6
        cpu = CPU(ROM(b'\xfd\xcb\x04\x76'), ram)
        cpu.ZFlag = Bits.reset()
        cpu.IY = 0x2000
        cpu.readOp()
        self.assertEqual(20, cpu.t_states)

    def test_bit_7_B_correctly_set_z_flag(self):
        cpu = CPU(ROM(b'\xcb\x78'))
        cpu.B = 0b10000000
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)

    def test_bit_7_B_correctly_reset_z_flag(self):
        cpu = CPU(ROM(b'\xcb\x78'))
        cpu.B = 0b01111111
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)
