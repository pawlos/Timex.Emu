import tests_suite
import os
import unittest

from cpu import CPU
from rom import ROM
from debugger import Debugger, HOOK_ADDR_ALL
from opcodes import Opcodes

ZEXALL_TESTS = os.environ.get('ZEXALL', False)
ZEXDOC_TESTS = os.environ.get('ZEXDOC', False)

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
        print(chr(c), end='', flush=True)

    def systemFunction9(self, cpu):
        idx = cpu.DE
        msg = ''
        while True:
            c = cpu.ram[idx]
            if chr(c) == '$':
                break
            msg += chr(c)
            idx += 1

        print(msg, end='', flush=True)

    def stop(self, cpu):
        raise Exception('Stop')

    def printIUT(self, cpu):
        pc = cpu.prev_pc
        opcode = cpu.ram[pc-1]
        print('{:04x}: AF: {:04x}, {:02x}'.format(pc, cpu.AF, opcode))
    
    def printIUT2B(self, cpu):
        pc = cpu.prev_pc
        opcode1 = cpu.ram[pc-1]
        opcode2 = cpu.ram[pc-2]
        opcode3 = cpu.ram[pc-3]
        opcode4 = cpu.ram[pc-4]
        print('{:04x}: AF: {:04x}, opcode: {:02x}{:02x}{:02x}{:02x}'.format(pc, cpu.AF, opcode4, opcode3, opcode2, opcode1))

    def print(self, cpu):
        print('{:04x}: AF: {:04x}, WZ: {:04x}, BC: {:04x}, DE: {:04x}, HL: {:04x}, SP: {:04x}, IX: {:04x}, IY: {:04x}'.format(
            cpu.prev_pc, cpu.AF, cpu.WZ, cpu.BC, cpu.DE, cpu.HL, cpu.SP, cpu.IX, cpu.IY))


    @unittest.skipUnless(ZEXDOC_TESTS, "ZEXDOC_TEST is not set")
    def test_zexdoc(self):
        print(">>> RUNNING ZEXDOC")
        debugger = Debugger()
        debugger.stopOnError = False
        debugger.setHook(0x5, self.systemFunction)
        debugger.setHook(0x0, self.stop)
        rom = ROM(mapAt=0x100)
        rom.loadFrom('./zexdoc.com', False)
        cpu = CPU(rom=rom,debugger=debugger)        
        print(f'Value: {cpu.ram[0x120]:02x}')
        cpu.SP = 0xF000
        cpu.run(0x100)
        self.assertTrue(True)

    @unittest.skipUnless(ZEXALL_TESTS, "ZEXALL_TEST is not set")
    def test_zexall(self):
        print(">>> RUNNING ZEXALL")
        debugger = Debugger()
        debugger.stopOnError = False
        debugger.setHook(0x5, self.systemFunction)
        debugger.setHook(0x0, self.stop)

        rom = ROM(mapAt=0x100)
        rom.loadFrom('./zexall.com', False)
        cpu = CPU(rom=rom,debugger=debugger)        
        cpu.SP = 0xF000
        cpu.run(0x100)
        self.assertTrue(True)


def suite():
    return unittest.TestLoader().discover(".", pattern="*.py")

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
