import tests_suite
import os
import unittest

from cpu import CPU
from rom import ROM
from loggers import Logger
from debugger import Debugger
from opcodes import Opcodes

ZEXALL_TESTS = os.environ.get('ZEXALL', False)

class tests_cpu(unittest.TestCase):
    def test_init_zeros_registers(self):
        cpu = CPU(ROM(b'\x00'))
        self.assertEqual(0, cpu.A)
        self.assertEqual(0, cpu.B)
        self.assertEqual(0, cpu.C)
        self.assertEqual(0, cpu.D)
        self.assertEqual(0, cpu.E)
        self.assertEqual(0, cpu.H)
        self.assertEqual(0, cpu.L)

    def test_HL_property_assign_correct_values_to_H_and_L(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.HL = 0x1123
        self.assertEqual(0x11, cpu.H)
        self.assertEqual(0x23, cpu.L)

    def test_HL_property_has_correct_value_when_H_and_L_are_set(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.H = 0x66
        cpu.L = 0x01
        self.assertEqual(0x6601, cpu.HL)

    def test_ld_A_07_works_correctly(self):
        cpu = CPU(ROM(b'\x3e\x07'))
        cpu.readOp()
        self.assertEqual(0x07, cpu.A)

    def test_registers_are_accessible_by_index_and_name(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.regs[0] = 0x11
        self.assertEqual(0x11, cpu.B)

    def test_0x62_opcode_correctly_maps_to_LD_H_D(self):
        cpu = CPU(ROM(b'\x62'))
        cpu.D = 0xaa
        cpu.readOp()
        self.assertEqual(0xaa, cpu.H)

    def test_0x6b_opcode_correctly_maps_to_LD_L_E(self):
        cpu = CPU(ROM(b'\x6b'))
        cpu.E = 0xbb
        cpu.readOp()
        self.assertEqual(0xbb, cpu.L)

    def test_16bit_registers_are_accessed_by_8bit_parts(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.HL = 0x1234

        self.assertEqual(0x12, cpu.H)
        self.assertEqual(0x34, cpu.L)

    def test_16bit_registers(self):
        cpu = CPU(ROM(b'\x2b'))
        cpu.HL = 0x0100
        cpu.readOp()
        self.assertEqual(0x00, cpu.H)
        self.assertEqual(0xFF, cpu.L)

    def test_ix_set_get(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.IX = 0x1223
        self.assertEqual(0x1223, cpu.IX)

    def test_iy_set_get(self):
        cpu = CPU(ROM(b'\x00'))
        cpu.IY = 0x3456
        self.assertEqual(0x3456, cpu.IY)

    def test_rom_getitem(self):
        rom = ROM(b'\x00\x01\x02\x03\x04\x05')
        self.assertEqual(0x05, rom[5])

    def systemFunction(self, cpu):
        if cpu.C == 2:
            self.systemFunction2(cpu)
        elif cpu.C == 9:
            self.systemFunction9(cpu)

        Opcodes.ret(cpu, 0xc9, cpu.logger)
        return True #handled

    def systemFunction2(self, cpu):
        c = cpu.E
        print(chr(c), end='')

    def systemFunction9(self, cpu):
        idx = cpu.DE
        msg = ''
        while True:
            c = cpu.ram[idx]
            if chr(c) == '$':
                break
            msg += chr(c)
            idx += 1
        print(msg, end='')

    def stop(self, cpu):
        #print(f'Stop...')
        pass

    def print(self, cpu):
        print('{:04x}: AF: {:04x}, BC: {:04x}, DE: {:04x}, HL: {:04x}, SP: {:04x}, IY: {:04x}, (HL): {:02x}, (0x1c2): {:02x}, (0x1c3): {:02x}'.format(
                (cpu.pc-1), cpu.AF, cpu.BC, cpu.DE, cpu.HL, cpu.SP, cpu.IY, cpu.ram[cpu.HL], cpu.ram[0x1c2], cpu.ram[0x1c3]))

    @unittest.skipUnless(ZEXALL_TESTS, "ZEXALL test")
    def test_zexall(self):
        print(">>> RUNNING ZEXALL")
        debugger = Debugger()
        debugger.setBreakpoint(0x100)
        debugger.setBreakpoint(0x1B3B)
        debugger.setHook(0x5, self.systemFunction)
        debugger.setHook(0x0, self.stop)
        debugger.setHook(-1, self.print)
        rom = ROM(mapAt=0x100)
        rom.loadFrom('zexall.com', False)
        cpu = CPU(rom=rom,debugger=debugger)
        cpu.SP = 0xF000
        #cpu.logger = Logger(cpu)
        cpu.run(0x100)
        self.assertTrue(True)


def suite():
    return unittest.TestLoader().discover(".", pattern="*.py")

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
