import tests_suite

import unittest
from cpu import CPU
from rom import ROM


class tests_interrupts(unittest.TestCase):
    def test_di(self):
        cpu = CPU(ROM(b'\xf3'))
        cpu.readOp()

        self.assertEqual(0x00, cpu.iff1)

    def test_di_(self):
        cpu = CPU(ROM(b'\xfb'))
        cpu.readOp()

        self.assertEqual(0x01, cpu.iff1)
