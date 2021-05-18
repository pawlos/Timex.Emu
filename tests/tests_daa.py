import tests_suite

import unittest
from cpu import CPU
from rom import ROM

@unittest.skip("DAA not yet implemented")
class tests_daa(unittest.TestCase):

    def test_daa_correctly_fixes_the_value_in_A_for_addition(self):        
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0b1010
        cpu.readOp()
        self.assertEqual(0b10000, cpu.A)

    def test_daa_does_not_affect_value_of_adding_1_and_1(self):
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0b0010
        cpu.readOp()
        self.assertEqual(0b0010, cpu.A)

    def test_daa_correctly_fixes_the_value_in_A_for_2_digits_additions(self):
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0b01000001
        cpu.readOp()
        self.assertEqual(0b01000111, cpu.A)

    def test_daa_correctly_fixes_the_value_in_A_for_subtraction(self):
        cpu = CPU(ROM(b'\x27'))
        cpu.A = 0b11111
        cpu.readOp()
        self.assertEqual(0b11001, cpu.A)
