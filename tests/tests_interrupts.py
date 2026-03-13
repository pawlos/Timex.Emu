import tests_suite

import unittest
from cpu import CPU
from ram import RAM
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

    def test_checkInterrupts_pushes_pc_and_decrements_sp(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00' * 0x4000), ram)
        cpu.pc = 0x1234
        cpu.SP = 0x6000
        cpu.iff1 = 1
        cpu.im = 1
        # trigger interrupt
        cpu.generateInterrupt()
        cpu._checkInterrupts()
        # SP should be decremented by 2
        self.assertEqual(0x5FFE, cpu.SP)
        # return address 0x1234 on stack: high byte at SP+1, low byte at SP
        self.assertEqual(0x34, ram[0x5FFE])  # low byte
        self.assertEqual(0x12, ram[0x5FFF])  # high byte
        # should jump to 0x0038 in IM 1
        self.assertEqual(0x0038, cpu.pc)
