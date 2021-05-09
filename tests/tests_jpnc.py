import tests_suite

import unittest
from cpu import CPU
from rom import ROM
from utility import Bits


class tests_jpnc(unittest.TestCase):

    def test_jp_nc_jumps_if_CFlag_is_reset(self):
        rom = b'\x00'*0x480 + b'\x30\x00'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x480
        cpu.CFlag = False
        cpu.readOp()
        self.assertEqual(0x482, cpu.PC)

    def test_jp_nc_does_not_jump_if_CFlag_is_set(self):
        cpu = CPU(ROM(b'\x30\x00'))
        cpu.CFlag = True
        cpu.readOp()
        self.assertEqual(0x02, cpu.PC)

    def test_jp_nc_takes_2_m_cycles_if_condition_is_not_met(self):
        cpu = CPU(ROM(b'\x30\x00'))
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_jp_nc_takes_7_t_states_if_condition_is_not_met(self):
        cpu = CPU(ROM(b'\x30\x00'))
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_jp_nc_takes_3_m_cycles_if_condition_is_met(self):
        cpu = CPU(ROM(b'\x30\x00'))
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_jp_nc_takes_12_t_states_if_condition_is_met(self):
        cpu = CPU(ROM(b'\x30\x00'))
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(12, cpu.t_states)
