import sys
sys.path.append('../python')

import unittest
from cpu import CPU
from rom import ROM


class tests_cpu(unittest.TestCase):
    def test_init_zeros_registers(self):
        cpu = CPU(ROM('\x00'))
        self.assertEqual(0, cpu.A)
        self.assertEqual(0, cpu.B)
        self.assertEqual(0, cpu.C)
        self.assertEqual(0, cpu.D)
        self.assertEqual(0, cpu.E)
        self.assertEqual(0, cpu.H)
        self.assertEqual(0, cpu.L)

    def test_HL_property_assign_correct_values_to_H_and_L(self):
        cpu = CPU(ROM('\x00'))
        cpu.HL = 0x1123
        self.assertEqual(0x11, cpu.H)
        self.assertEqual(0x23, cpu.L)

    def test_HL_property_has_correct_value_when_H_and_L_are_set(self):
        cpu = CPU(ROM('\x00'))
        cpu.H = 0x66
        cpu.L = 0x01
        self.assertEqual(0x6601, cpu.HL)

    def test_ld_A_07_works_correctly(self):
        cpu = CPU(ROM('\x3e\x07'))
        cpu.readOp()
        self.assertEqual(0x07, cpu.A)

    def test_registers_are_accessible_by_index_and_name(self):
        cpu = CPU(ROM('\x00'))
        cpu.regs[0] = 0x11
        self.assertEqual(0x11, cpu.B)

    def test_0x62_opcode_correctly_maps_to_LD_H_D(self):
        cpu = CPU(ROM('\x62'))
        cpu.D = 0xaa
        cpu.readOp()
        self.assertEqual(0xaa, cpu.H)

    def test_0x6b_opcode_correctly_maps_to_LD_L_E(self):
        cpu = CPU(ROM('\x6b'))
        cpu.E = 0xbb
        cpu.readOp()
        self.assertEqual(0xbb, cpu.L)

    def test_16bit_registers_are_accessed_by_8bit_parts(self):
        cpu = CPU(ROM('\x00'))
        cpu.HL = 0x1234

        self.assertEqual(0x12, cpu.H)
        self.assertEqual(0x34, cpu.L)

    def test_16bit_registers(self):
        cpu = CPU(ROM('\x2b'))
        cpu.HL = 0x0100
        cpu.readOp()
        self.assertEqual(0x00, cpu.H)
        self.assertEqual(0xFF, cpu.L)

    def test_ix_set_get(self):
        cpu = CPU(ROM('\x00'))
        cpu.IX = 0x1223
        self.assertEqual(0x1223, cpu.IX)

    def test_iy_set_get(self):
        cpu = CPU(ROM('\x00'))
        cpu.IY = 0x3456
        self.assertEqual(0x3456, cpu.IY)

    def test_rom_getitem(self):
        rom = ROM('\x00\x01\x02\x03\x04\x05')
        self.assertEqual(0x05, rom[5])


def suite():
    return unittest.TestLoader().discover(".", pattern="*.py")

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
