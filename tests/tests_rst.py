import tests_suite

import unittest
from cpu import CPU
from ram import RAM
from rom import ROM


class tests_rst(unittest.TestCase):

    def test_rst_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xdf'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x18, cpu.PC)

    def test_rst_0_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xc7'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x0, cpu.PC)

    def test_rst_8_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xcf'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x08, cpu.PC)

    def test_rst_10_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xd7'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x10, cpu.PC)

    def test_rst_20_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xe7'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x20, cpu.PC)

    def test_rst_28_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xef'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x28, cpu.PC)

    def test_rst_30_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xf7'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x30, cpu.PC)

    def test_rst_38_does_sets_PC_correctly(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xff'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(0x38, cpu.PC)

    def test_rst_takes_3_m_cycles(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xff'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(3, cpu.m_cycles)

    def test_rst_takes_11_t_states(self):
        ram = RAM()
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xff'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        self.assertEqual(11, cpu.t_states)

    def test_rst_pushes_correct_return_address(self):
        ram = RAM()
        # RST 18h (0xDF) at address 0x15B3
        # After reading opcode, PC = 0x15B4, which is the return address
        cpu = CPU(ROM(b'\x00'*0x15b3+b'\xdf'), ram)
        cpu.PC = 0x15B3
        cpu.SP = 0x2000
        cpu.readOp()
        # return address 0x15B4 should be on the stack
        # low byte at SP, high byte at SP+1
        self.assertEqual(0xB4, ram[0x1FFE])  # low byte of 0x15B4
        self.assertEqual(0x15, ram[0x1FFF])  # high byte of 0x15B4
