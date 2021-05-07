import unittest
from cpu import CPU
from rom import ROM
from utility import Bits


class tests_jp(unittest.TestCase):

    def test_jp_nz_jumps_if_ZFlag_is_non_zero(self):
        rom = b'\x00' * 0x0480+b'\x20\xFA'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0480
        cpu.ZFlag = False
        cpu.readOp()
        self.assertEqual(0x047C, cpu.PC)

    def test_jp_nz_does_not_jump_if_ZFlag_is_set(self):
        cpu = CPU(ROM(b'\x20\xFA'))
        cpu.ZFlag = True
        cpu.readOp()
        self.assertEqual(0x02, cpu.PC)

    def test_jp_hl_does_set_ip_to_value_of_hl(self):
        cpu = CPU(ROM(b'\xe9'))
        cpu.HL = 0x4800
        cpu.readOp()
        self.assertEqual(0x4800, cpu.PC)

    def test_jp_e_does_set_ip_to_value_of_e(self):
        cpu = CPU(ROM(b'\x00'*0x480+b'\x18\x03'))
        cpu.PC = 0x480
        cpu.readOp()
        self.assertEqual(0x485, cpu.PC)

    def test_jp_ix_does_set_ip_to_value_of_ix(self):
        cpu = CPU(ROM(b'\xdd\xe9'))
        cpu.IX = 0x4600
        cpu.readOp()
        self.assertEqual(0x4600, cpu.PC)

    def test_jp_iy_does_set_ip_to_value_of_iy(self):
        cpu = CPU(ROM(b'\xfd\xe9'))
        cpu.IY = 0x4622
        cpu.readOp()
        self.assertEqual(0x4622, cpu.PC)

    def test_jr_e_takes_3_m_cycles(self):
        cpu = CPU(ROM(b'\x00'*0x480+b'\x18\x03'))
        cpu.PC = 0x480
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_jr_e_takes_12_t_states(self):
        cpu = CPU(ROM(b'\x00'*0x480+b'\x18\x03'))
        cpu.PC = 0x480
        cpu.readOp()
        self.assertEqual(12, cpu.t_states)

    def test_jp_hl_does_take_1_m_cycle(self):
        cpu = CPU(ROM(b'\xe9'))
        cpu.HL = 0x4800
        cpu.readOp()
        self.assertEqual(1, cpu.m_cycles)

    def test_jp_hl_does_take_4_t_states(self):
        cpu = CPU(ROM(b'\xe9'))
        cpu.HL = 0x4800
        cpu.readOp()
        self.assertEqual(4, cpu.t_states)

    def test_jp_ix_does_take_2_m_cycles(self):
        cpu = CPU(ROM(b'\xdd\xe9'))
        cpu.IX = 0x4600
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_jp_ix_does_take_8_t_states(self):
        cpu = CPU(ROM(b'\xdd\xe9'))
        cpu.IX = 0x4600
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)

    def test_jp_iy_does_take_2_m_cycles(self):
        cpu = CPU(ROM(b'\xfd\xe9'))
        cpu.IY = 0x4622
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_jp_iy_does_take_8_t_states(self):
        cpu = CPU(ROM(b'\xfd\xe9'))
        cpu.IY = 0x4622
        cpu.readOp()
        self.assertEqual(8, cpu.t_states)

    def test_jp_nz_jumps_takes_3_m_cycles_if_jump_is_taken(self):
        rom = b'\x00' * 0x0480+b'\x20\xFA'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0480
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_jp_nz_jumps_takes_12_t_states_if_jump_is_taken(self):
        rom = b'\x00' * 0x0480+b'\x20\xFA'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0480
        cpu.ZFlag = Bits.reset()
        cpu.readOp()
        self.assertEqual(12, cpu.t_states)

    def test_jp_nz_jumps_takes_2_m_cycles_if_jump_is_not_taken(self):
        rom = b'\x00' * 0x0480+b'\x20\xFA'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0480
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(2, cpu.m_cycles)

    def test_jp_nz_jumps_takes_7_t_states_if_jump_is_taken(self):
        rom = b'\x00' * 0x0480+b'\x20\xFA'
        cpu = CPU(ROM(rom))
        cpu.PC = 0x0480
        cpu.ZFlag = Bits.set()
        cpu.readOp()
        self.assertEqual(7, cpu.t_states)

    def test_JP_XX_sets_PC_correctly(self):
        cpu = CPU(ROM(b'\xc3\xcb\x11'))
        cpu.PC = 0
        cpu.readOp()
        self.assertEqual(0x11cb, cpu.PC)

    def test_JP_XX_takes_3_m_cycles(self):
        cpu = CPU(ROM(b'\xc3\xcb\x11'))
        cpu.PC = 0
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_JP_XX_takes_10_t_states(self):
        cpu = CPU(ROM(b'\xc3\xcb\x11'))
        cpu.PC = 0
        cpu.readOp()
        self.assertEqual(10, cpu.t_states)
