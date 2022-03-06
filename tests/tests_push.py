import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_push(unittest.TestCase):

    def test_push_correctly_stores_af_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_hl_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xE5'), ram)
        cpu.HL = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_bc_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xC5'), ram)
        cpu.BC = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_de_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xD5'), ram)
        cpu.DE = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_takes_3_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_push_takes_11_t_states(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(11, cpu.t_states)

    def test_push_ix_stores_value_from_IX(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xdd\xe5'), ram)
        cpu.IX = 0x1122
        cpu.SP = 0x1007
        cpu.readOp()
        self.assertEqual(0x11, ram[0x1006])
        self.assertEqual(0x22, ram[0x1005])

    def test_push_iy_stores_value_from_IY(self):
        ram = RAM()
        cpu = CPU(ROM(b'\xfd\xe5'), ram)
        cpu.IY = 0x3344
        cpu.SP = 0x1007
        cpu.readOp()
        self.assertEqual(0x33, ram[0x1006])
        self.assertEqual(0x44, ram[0x1005])
