import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_push(unittest.TestCase):

    def test_push_correctly_stores_af_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM('\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_hl_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM('\xE5'), ram)
        cpu.HL = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_bc_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM('\xC5'), ram)
        cpu.BC = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_correctly_stores_de_on_stack(self):
        ram = RAM()
        cpu = CPU(ROM('\xD5'), ram)
        cpu.DE = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(0x22, ram[0x1006])
        self.assertEqual(0x33, ram[0x1005])

    def test_push_takes_3_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM('\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_push_takes_11_t_states(self):
        ram = RAM()
        cpu = CPU(ROM('\xF5'), ram)
        cpu.AF = 0x2233
        cpu.SP = 0x1007

        cpu.readOp()
        self.assertEqual(11, cpu.t_states)
