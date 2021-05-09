import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_ld_nn_a(unittest.TestCase):

    def test_ld_nn_a_correctly_stores_value_at_given_address(self):
        cpu = CPU(ROM(b'\x32\x31\x41'))
        cpu.A = 0xD7
        cpu.readOp()
        self.assertEqual(0xD7, cpu.ram[0x3141])

    def test_ld_nn_a_does_not_affect_flags(self):
        cpu = CPU(ROM(b'\x32\xb2\x29'))
        cpu.HFlag = False
        cpu.ZFlag = True
        cpu.PVFlag = False
        cpu.SFlag = True

        self.assertFalse(cpu.HFlag)
        self.assertTrue(cpu.ZFlag)
        self.assertFalse(cpu.PVFlag)
        self.assertTrue(cpu.SFlag)

    def test_ld_nn_takes_4_m_cycles(self):
        cpu = CPU(ROM(b'\x32\x31\x41'))
        cpu.A = 0xD7
        cpu.readOp()
        self.assertEqual(4, cpu.m_cycles)

    def test_ld_nn_takes_13_t_states(self):
        cpu = CPU(ROM(b'\x32\x31\x41'))
        cpu.A = 0xD7
        cpu.readOp()
        self.assertEqual(13, cpu.t_states)
