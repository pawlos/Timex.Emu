import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_cpdr(unittest.TestCase):

    def test_cpdr_decrements_wz(self):
        # CPDR (ED B9) searches backwards, WZ should be decremented
        ram = RAM()
        ram[0x5000] = 0x42  # value to find
        cpu = CPU(ROM(b'\xed\xb9'), ram)
        cpu.A = 0x42
        cpu.HL = 0x5000
        cpu.BC = 0x0001
        cpu.WZ = 0x1000
        cpu.readOp()
        self.assertEqual(0x0FFF, cpu.WZ)  # WZ should be decremented
