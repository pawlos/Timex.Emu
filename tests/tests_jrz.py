import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_jrz(unittest.TestCase):

    def test_jr_z_jumps_backward_when_z_set(self):
        # JR Z, -4 at address 0x0010
        # opcode 0x28, displacement 0xFC (-4)
        # Jump target = 0x0012 + (-4) = 0x000E
        ram = RAM()
        cpu = CPU(ROM(b'\x00' * 0x10 + b'\x28\xfc'), ram)
        cpu.PC = 0x0010
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x000E, cpu.PC)

    def test_jr_z_jumps_if_ZFlag_is_set(self):
        rom = b'\x00' * 0x0300+b'\x28\x03'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0300
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x0305, cpu.PC)

    def test_jr_z_does_not_jump_if_ZFlag_is_reset(self):
        cpu = CPU(ROM(b'\x28\x00'))
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x02, cpu.PC)

    def test_jr_z_does_not_change_the_z_flag(self):
        cpu = CPU(ROM(b'\x28\x00\x28\x00'))
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertFalse(cpu.ZFlag)
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertTrue(cpu.ZFlag)

    def test_jr_z_takes_2_m_cycles_if_condition_is_not_met(self):
        cpu = CPU(ROM(b'\x28\x00'))
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_jr_z_takes_7_t_states_if_condition_is_not_met(self):
        cpu = CPU(ROM(b'\x28\x00'))
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_jr_z_takes_3_m_cycles_if_condition_is_met(self):
        cpu = CPU(ROM(b'\x28\x00'))
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_jr_z_takes_12_t_states_if_condition_is_met(self):
        cpu = CPU(ROM(b'\x28\x00'))
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(12, cpu.t_states)
