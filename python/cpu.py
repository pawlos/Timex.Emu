#Z80 CPU

from opcodes import *
from regs import *
from ram import *
from rom import *
from loggers import EmptyLogger
from debugger import EmptyDebugger
from ioports import IOPorts
from utility import Bits
from known_addresses import *
from dispatch_tables import (build_base_table, build_cb_table,
    build_dd_table, build_ed_table, build_fd_table,
    build_ddcb_table, build_fdcb_table)


def _reg8(index):
    def getter(self): return self.regs[index]
    def setter(self, value): self.regs[index] = Bits.limitTo8Bits(value)
    return property(getter, setter)

def _reg8_attr(attr):
    def getter(self): return getattr(self, attr)
    def setter(self, value): setattr(self, attr, Bits.limitTo8Bits(value))
    return property(getter, setter)

def _reg16(hi, lo):
    def getter(self): return (self.regs[hi] << 8) + self.regs[lo]
    def setter(self, value):
        value = Bits.limitTo16Bits(value)
        self.regs[hi] = value >> 8
        self.regs[lo] = Bits.limitTo8Bits(value)
    return property(getter, setter)

def _reg16_prim(hi, lo):
    def getter(self): return (self.regsPri[hi] << 8) + self.regsPri[lo]
    def setter(self, value):
        value = Bits.limitTo16Bits(value)
        self.regsPri[hi] = value >> 8
        self.regsPri[lo] = Bits.limitTo8Bits(value)
    return property(getter, setter)

def _reg16_attr(attr):
    def getter(self): return getattr(self, attr)
    def setter(self, value): setattr(self, attr, Bits.limitTo16Bits(value))
    return property(getter, setter)

def _flag(bit):
    def getter(self): return Bits.getNthBit(self.F, bit) == 1
    def setter(self, value): self.F = Bits.setNthBit(self.F, bit, 1 if value else 0)
    return property(getter, setter)


class CPU(object):

    rst_jumps = {0: 0x00, 1: 0x08, 2: 0x10, 3: 0x18, 4: 0x20,
                 5: 0x28, 6: 0x30, 7: 0x38}

    # 16-bit register pairs (must be defined before 8-bit to avoid name collision)
    # Using raw indices: B=0,C=1,D=2,E=3,H=4,L=5,A=7,F=8
    HL = _reg16(4, 5); BC = _reg16(0, 1)
    DE = _reg16(2, 3); AF = _reg16(7, 8)

    # 16-bit prime register pairs
    HLPrim = _reg16_prim(4, 5); BCPrim = _reg16_prim(0, 1)
    DEPrim = _reg16_prim(2, 3); AFPrim = _reg16_prim(7, 8)

    # 16-bit direct attribute registers
    SP = _reg16_attr('sp')
    IX = _reg16_attr('ix')
    IY = _reg16_attr('iy')

    # 8-bit registers (from regs array)
    A = _reg8(7); F = _reg8(8)
    B = _reg8(0); C = _reg8(1)
    D = _reg8(2); E = _reg8(3)
    H = _reg8(4); L = _reg8(5)

    # 8-bit registers (direct attributes)
    R = _reg8_attr('r')
    W = _reg8_attr('w')
    Z = _reg8_attr('z')
    I = _reg8_attr('i')

    # Flags (bit positions: CF=0,NF=1,PVF=2,XF=3,HF=4,YF=5,ZF=6,SF=7)
    ZFlag = _flag(6); CFlag = _flag(0)
    NFlag = _flag(1); HFlag = _flag(4)
    SFlag = _flag(7); PVFlag = _flag(2)
    YFlag = _flag(5); XFlag = _flag(3)

    @property
    def PC(self):
        value = self.pc
        self.pc = (self.pc + 1) & 0xFFFF
        return value

    @PC.setter
    def PC(self, value):
        self.pc = Bits.limitTo16Bits(value)

    @property
    def WZ(self):
        return (self.W << 8) + self.Z

    @WZ.setter
    def WZ(self, value):
        self.W = Bits.limitTo8Bits(value >> 8)
        self.Z = Bits.limitTo8Bits(value)

    def Reg16(self, index, value=None, ix=False, iy=False, af=False):
        if value is None:
            if index == 0:
                return self.BC
            elif index == 1:
                return self.DE
            elif index == 2:
                if not ix and not iy:
                    return self.HL
                elif ix:
                    return self.IX
                elif iy:
                    return self.IY
            elif index == 3 and not af:
                return self.SP
            elif index == 3 and af:
                return self.AF
        else:
            value = Bits.limitTo16Bits(value)
            if index == 0:
                self.BC = value
                return self.BC
            elif index == 1:
                self.DE = value
                return self.DE
            elif index == 2:
                if not ix and not iy:
                    self.HL = value
                    return self.HL
                elif ix:
                    self.IX = value
                    return self.IX
                elif iy:
                    self.IY = value
                    return self.IY
            elif index == 3 and not af:
                self.SP = value
                return self.SP
            elif index == 3 and af:
                self.AF = value
                return self.AF

    @property
    def t_states(self):
        return self.tstates

    @t_states.setter
    def t_states(self, value):
        self.tstates += value

    @property
    def m_cycles(self):
        return self.mcycles

    @m_cycles.setter
    def m_cycles(self, value):
        self.mcycles += value

    def reset(self):
        #Index registers
        self.ix = 0x00
        self.iy = 0x00
        self.sp = 0x7FFF
        self.pc = 0x00
        #special registers
        self.i = 0x00
        self.r = 0x00
        self.w = 0x00
        self.z = 0x00

        self.halted = Bits.reset()
        self._interruptPending = False
        self.iff1 = 0x00
        self.iff2 = 0x00

        self.im = 0
                    #B,C,D,E,H,L,none,A, F
        self.regs = [0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00,
                     0xFF,
                     0x00,
                     0x00]
                    #B',C',D',E',H',L',none,A',F'
        self.regsPri = [0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0xFF,
                        0x00,
                        0x00]
        self.tstates = 0
        self.mcycles = 0

    def __init__(self,
                 rom=ROM(),
                 ram=RAM(),
                 logger=EmptyLogger(),
                 debugger=EmptyDebugger()):

        self.logger = logger
        self.debugger = debugger

        self.io = IOPorts()

        self.reset()

        self.ram = ram
        self.ram.load(rom)

        self.baseTable = build_base_table()
        self.cbTable = build_cb_table()
        self.ddTable = build_dd_table()
        self.edTable = build_ed_table()
        self.fdTable = build_fd_table()
        self.ddcbTable = build_ddcb_table()
        self.fdcbTable = build_fdcb_table()

        # Wire prefix opcodes to dispatch methods
        self.baseTable[0xCB] = self._dispatchCB
        self.baseTable[0xDD] = self._dispatchDD
        self.baseTable[0xED] = self._dispatchED
        self.baseTable[0xFD] = self._dispatchFD
        # Wire DDCB/FDCB in their prefix tables
        self.ddTable[0xCB] = self._dispatchDDCB
        self.fdTable[0xCB] = self._dispatchFDCB


    def generateInterrupt(self):
        self._interruptPending = True

    def readOp(self):
        self.prev_pc = self.PC
        pc = self.prev_pc
        opcode = self.ram[pc]
        handler = self.baseTable[opcode]
        if handler is None:
            self._missingOpcode(pc, opcode)
            return
        handled = self.debugger.next_opcode(pc, self)
        if handled:
            return
        handler(self, opcode, self.logger)

    def _dispatchPrefix(self, table, pc, prefix_opcode):
        sub = self.ram[pc]
        self.pc += 1
        fullOpcode = (prefix_opcode << 8) + sub
        try:
            handler = table[sub]
        except (KeyError, TypeError):
            handler = None
        if handler is None:
            self._missingOpcode(pc, fullOpcode)
            return
        self.debugger.next_opcode(pc, self)
        handler(self, fullOpcode, self.logger)

    def _dispatchCB(self, cpu, opcode, logger):
        self._dispatchPrefix(self.cbTable, self.pc, 0xCB)

    def _dispatchDD(self, cpu, opcode, logger):
        self._dispatchPrefix(self.ddTable, self.pc, 0xDD)

    def _dispatchED(self, cpu, opcode, logger):
        self._dispatchPrefix(self.edTable, self.pc, 0xED)

    def _dispatchFD(self, cpu, opcode, logger):
        self._dispatchPrefix(self.fdTable, self.pc, 0xFD)

    def _dispatchIndexedCB(self, table, cpu, opcode, logger):
        pc = self.PC  # consume displacement byte (auto-increments)
        displacement = cpu.ram[pc]
        fourthbyte = cpu.ram[cpu.PC]  # consume operation byte
        fullOpcode = (opcode << 16) + (displacement << 8) + fourthbyte
        handler = table[fourthbyte]
        if handler is None:
            self._missingOpcode(pc, fullOpcode)
            return
        self.debugger.next_opcode(pc, self)
        handler(self, fullOpcode, self.logger)

    def _dispatchDDCB(self, cpu, opcode, logger):
        self._dispatchIndexedCB(self.ddcbTable, cpu, opcode, logger)

    def _dispatchFDCB(self, cpu, opcode, logger):
        self._dispatchIndexedCB(self.fdcbTable, cpu, opcode, logger)

    def _missingOpcode(self, pc, opcode):
        print("Missing opcode key: {1:x}, PC = 0x{0:x}".format(pc, opcode))
        if hasattr(self.debugger, 'stopOnError') and self.debugger.stopOnError:
            self.debugger.stop(self)

    def _checkInterrupts(self):
        if self.iff1 and self._interruptPending:
            self._interruptPending = False
            self.halted = Bits.reset()
            self.iff1 = Bits.reset()
            self.iff2 = Bits.reset()
            self.SP -= 1
            self.ram[self.SP] = self.pc >> 8
            self.SP -= 1
            self.ram[self.SP] = Bits.limitTo8Bits(self.pc)
            self.R += 1
            if self.im == 0 or self.im == 1:
                self.PC = 0x0038
            elif self.im == 2:
                vector_addr = (self.i << 8) | 0xFF
                low = self.ram[vector_addr]
                high = self.ram[(vector_addr + 1) & 0xFFFF]
                target = (high << 8) | low
                self.PC = target

    def run(self, pc=0x0):
        self.pc = pc
        while True:
            if not self.halted:
                self.readOp()
            else:
                self.m_cycles, self.t_states = 1, 4
            self._checkInterrupts()
