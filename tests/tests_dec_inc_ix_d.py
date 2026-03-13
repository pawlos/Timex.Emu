import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_dec_inc_ix_d(unittest.TestCase):

    def test_dec_ix_negative_displacement(self):
        # DEC (IX-1) -- DD 35 FF (FF = -1 signed)
        ram = RAM()
        ram[0x2FFF] = 0x05
        cpu = CPU(ROM(b'\xdd\x35\xff'), ram)
        cpu.IX = 0x3000
        cpu.readOp()
        # Should decrement at IX-1 (0x2FFF), not IX+255 (0x30FF)
        self.assertEqual(0x04, ram[0x2FFF])

    def test_inc_ix_negative_displacement(self):
        # INC (IX-1) -- DD 34 FF (FF = -1 signed)
        ram = RAM()
        ram[0x2FFF] = 0x05
        cpu = CPU(ROM(b'\xdd\x34\xff'), ram)
        cpu.IX = 0x3000
        cpu.readOp()
        # Should increment at IX-1 (0x2FFF), not IX+255 (0x30FF)
        self.assertEqual(0x06, ram[0x2FFF])
