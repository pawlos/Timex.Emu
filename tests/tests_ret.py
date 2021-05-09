import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM
from utility import Bits


class tests_ret(unittest.TestCase):

    def test_ret_does_sets_PC_correctly(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc9'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_reset(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_nz_does_sets_PC_correctly_if_Zflag_is_set(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x3536, cpu.PC)
        self.assertEqual(0x4000, cpu.SP)

    def test_ret_z_does_sets_PC_correctly_if_Zflag_is_set(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc8'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x18B5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_z_does_sets_PC_correctly_if_Zflag_is_reset(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc8'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x3536, cpu.PC)
        self.assertEqual(0x4000, cpu.SP)

    def test_ret_nc_does_sets_PC_correctly_if_Cflag_is_reset(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xd0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.CFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_c_does_sets_PC_correctly_if_Cflag_is_set(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xd8'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.CFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_po_does_sets_PC_correctly_if_PVflag_is_reset(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xe0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.PVFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_po_does_sets_PC_correctly_if_PVflag_is_set(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xe8'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.PVFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_p_does_sets_PC_correctly_if_PVflag_is_reset(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_p_does_sets_PC_correctly_if_PVflag_is_set(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf8'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(0x18b5, cpu.PC)
        self.assertEqual(0x4002, cpu.SP)

    def test_ret_takes_3_m_cycles(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc9'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_ret_takes_10_t_states(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xc9'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)

    def test_ret_cc_does_takes_3_m_cycles_if_cc_is_true(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_ret_cc_does_takes_1_m_cycles_if_cc_is_false(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_ret_cc_does_takes_11_t_states_if_cc_is_true(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(11, cpu.t_states)

    def test_ret_cc_does_takes_5_t_states_if_cc_is_false(self):
        ram = RAM()
        ram[0x4000] = 0xB5
        ram[0x4001] = 0x18
        cpu = CPU(ROM(b'\x00'*0x3535+b'\xf0'), ram)
        cpu.PC = 0x3535
        cpu.SP = 0x4000
        cpu.SFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(5, cpu.t_states)
