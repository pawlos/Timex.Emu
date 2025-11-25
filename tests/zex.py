import os
import tests_suite

import unittest
from cpu import CPU
from rom import ROM
from debugger import Debugger, HOOK_ADDR_ALL
from utility import Bits
from opcodes import Opcodes



ZEXALL_TESTS = os.environ.get('ZEXALL', False)
ZEXDOC_TESTS = os.environ.get('ZEXDOC', False)

class tests_zex(unittest.TestCase):

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
    return unittest.TestLoader().discover(".", pattern="zex.py")

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
