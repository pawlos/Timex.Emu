import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_dec(unittest.TestCase):

    def test_dec_iy_sets_correct_value_is_set(self):
        ram = RAM()
        ram[0x10f] = 0xDD
        cpu = CPU(ROM('\xfd\x35\x0f'), ram)
        cpu.IY = 0x100
        cpu.readOp()
        self.assertEqual(0xDC, ram[cpu.IY+15])
