import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_hl_addr(unittest.TestCase):

    def test_ld_hl_A_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x77'), ram)
        cpu.HL = 0x2000
        cpu.A = 0x34
        cpu.readOp()
        self.assertEqual(0x34, ram[0x2000])

    def test_ld_hl_B_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x70'), ram)
        cpu.HL = 0x2000
        cpu.B = 0x34
        cpu.readOp()
        self.assertEqual(0x34, ram[0x2000])

    def test_ld_hl_C_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x71'), ram)
        cpu.HL = 0x2000
        cpu.C = 0x34
        cpu.readOp()
        self.assertEqual(0x34, ram[0x2000])

    def test_ld_hl_D_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x72'), ram)
        cpu.HL = 0x2000
        cpu.D = 0x34
        cpu.readOp()
        self.assertEqual(0x34, ram[0x2000])

    def test_ld_hl_E_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x73'), ram)
        cpu.HL = 0x2000
        cpu.E = 0x20
        cpu.readOp()
        self.assertEqual(0x20, ram[0x2000])

    def test_ld_hl_H_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x74'), ram)
        cpu.HL = 0x2000
        cpu.readOp()
        self.assertEqual(0x20, ram[0x2000])

    def test_ld_hl_L_correctly_stores_value_from_given_address_to_hl(self):
        ram = RAM()
        cpu = CPU(ROM('\x75'), ram)
        cpu.HL = 0x2000
        cpu.readOp()
        self.assertEqual(0x00, ram[0x2000])

    def test_ld_hl_L_takes_2_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM('\x75'), ram)
        cpu.HL = 0x2000
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_ld_hl_L_takes_7_t_states(self):
        ram = RAM()
        cpu = CPU(ROM('\x75'), ram)
        cpu.HL = 0x2000
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)
