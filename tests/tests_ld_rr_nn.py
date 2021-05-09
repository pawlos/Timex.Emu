import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_ld_rr_nn(unittest.TestCase):

    def test_ld_BC_nn_correctly_stores_value_to_BC(self):
        cpu = CPU(ROM(b'\x01\xba\xab'))
        cpu.readOp()
        self.assertEqual(0xabba, cpu.BC)

    def test_ld_DE_nn_correctly_stores_value_to_DE(self):
        cpu = CPU(ROM(b'\x11\xde\xc0'))
        cpu.readOp()
        self.assertEqual(0xc0de, cpu.DE)

    def test_ld_HL_nn_correctly_stores_value_to_HL(self):
        cpu = CPU(ROM(b'\x21\xfe\xca'))
        cpu.readOp()
        self.assertEqual(0xcafe, cpu.HL)

    def test_ld_SP_nn_correctly_stores_value_to_SP(self):
        cpu = CPU(ROM(b'\x31\x37\x13'))
        cpu.readOp()
        self.assertEqual(0x1337, cpu.SP)

    def test_ld_BC_addr_nn_correctly_loads_value_to_BC(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x4b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(0x7865, cpu.BC)

    def test_ld_DE_addr_nn_correctly_loads_value_to_DE(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x5b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(0x7865, cpu.DE)

    def test_ld_HL_addr_nn_correctly_loads_value_to_HL(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x6b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(0x7865, cpu.HL)

    def test_ld_SP_addr_nn_correctly_loads_value_to_SP(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x7b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(0x7865, cpu.SP)

    def test_ld_BC_addr_nn_takes_6_m_cycles(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x4b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(6, cpu.m_cycles)

    def test_ld_BC_addr_nn_takes_20_t_states(self):
        ram = RAM()
        ram[0x2130] = 0x65
        ram[0x2131] = 0x78
        cpu = CPU(ROM(b'\xED\x4b\x30\x21'), ram)
        cpu.readOp()
        self.assertEqual(20, cpu.t_states)
