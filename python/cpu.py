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


class CPU(object):

    rst_jumps = {0: 0x00, 1: 0x08, 2: 0x10, 3: 0x18, 4: 0x20,
                 5: 0x28, 6: 0x30, 7: 0x38}

    @property
    def A(self):
        return self.regs[A]

    @A.setter
    def A(self, value):
        self.regs[A] = Bits.limitTo8Bits(value)

    @property
    def F(self):
        return self.regs[F]

    @F.setter
    def F(self, value):
        self.regs[F] = Bits.limitTo8Bits(value)

    @property
    def B(self):
        return self.regs[B]

    @B.setter
    def B(self, value):
        self.regs[B] = Bits.limitTo8Bits(value)

    @property
    def C(self):
        return self.regs[C]

    @C.setter
    def C(self, value):
        self.regs[C] = Bits.limitTo8Bits(value)

    @property
    def D(self):
        return self.regs[D]

    @D.setter
    def D(self, value):
        self.regs[D] = Bits.limitTo8Bits(value)

    @property
    def E(self):
        return self.regs[E]

    @E.setter
    def E(self, value):
        self.regs[E] = Bits.limitTo8Bits(value)

    @property
    def H(self):
        return self.regs[H]

    @H.setter
    def H(self, value):
        self.regs[H] = Bits.limitTo8Bits(value)

    @property
    def L(self):
        return self.regs[L]

    @L.setter
    def L(self, value):
        self.regs[L] = Bits.limitTo8Bits(value)

    @property
    def R(self):
        return self.r

    @R.setter
    def R(self, value):
        self.r = Bits.limitTo8Bits(value)

    @property
    def W(self):
        return self.w

    @W.setter
    def W(self, value):
        self.w = Bits.limitTo8Bits(value)

    @property
    def Z(self):
        return self.z

    @Z.setter
    def Z(self, value):
        self.z = Bits.limitTo8Bits(value)

    @property
    def ZFlag(self):
        return Bits.getNthBit(self.F, ZF) == 1

    @ZFlag.setter
    def ZFlag(self, value):
        self.F = Bits.setNthBit(self.F, ZF, 1 if value else 0)

    @property
    def CFlag(self):
        return Bits.getNthBit(self.F, CF) == 1

    @CFlag.setter
    def CFlag(self, value):
        self.F = Bits.setNthBit(self.F, CF, 1 if value else 0)

    @property
    def NFlag(self):
        return Bits.getNthBit(self.F, NF) == 1

    @NFlag.setter
    def NFlag(self, value):
        self.F = Bits.setNthBit(self.F, NF, 1 if value else 0)

    @property
    def HFlag(self):
        return Bits.getNthBit(self.F, HF) == 1

    @HFlag.setter
    def HFlag(self, value):
        self.F = Bits.setNthBit(self.F, HF, 1 if value else 0)

    @property
    def SFlag(self):
        return Bits.getNthBit(self.F, SF) == 1

    @SFlag.setter
    def SFlag(self, value):
        self.F = Bits.setNthBit(self.F, SF, 1 if value else 0)

    @property
    def PVFlag(self):
        return Bits.getNthBit(self.F, PVF) == 1

    @PVFlag.setter
    def PVFlag(self, value):
        self.F = Bits.setNthBit(self.F, PVF, 1 if value else 0)

    @property
    def YFlag(self):
        return Bits.getNthBit(self.F, YF) == 1

    @YFlag.setter
    def YFlag(self, value: bool):
        self.F = Bits.setNthBit(self.F, YF, 1 if value else 0)

    @property
    def XFlag(self):
        return Bits.getNthBit(self.F, XF) == 1

    @XFlag.setter
    def XFlag(self, value: bool):
        self.F = Bits.setNthBit(self.F, XF, 1 if value else 0)

    @property
    def HL(self):
        return (self.regs[H] << 8) + self.regs[L]

    @HL.setter
    def HL(self, value):
        value = Bits.limitTo16Bits(value)
        self.regs[H] = value >> 8
        self.regs[L] = Bits.limitTo8Bits(value)

    @property
    def HLPrim(self):
        return (self.regsPri[H] << 8) + self.regsPri[L]

    @HLPrim.setter
    def HLPrim(self, value):
        value = Bits.limitTo16Bits(value)
        self.regsPri[H] = value >> 8
        self.regsPri[L] = Bits.limitTo8Bits(value)

    @property
    def DE(self):
        return (self.regs[D] << 8) + self.regs[E]

    @DE.setter
    def DE(self, value):
        value = Bits.limitTo16Bits(value)
        self.regs[D] = value >> 8
        self.regs[E] = Bits.limitTo8Bits(value)

    @property
    def DEPrim(self):
        return (self.regsPri[D] << 8) + self.regsPri[E]

    @DEPrim.setter
    def DEPrim(self, value):
        value = Bits.limitTo16Bits(value)
        self.regsPri[D] = value >> 8
        self.regsPri[E] = Bits.limitTo8Bits(value)

    @property
    def BC(self):
        return (self.regs[B] << 8) + self.regs[C]

    @BC.setter
    def BC(self, value):
        value = Bits.limitTo16Bits(value)
        self.regs[B] = value >> 8
        self.regs[C] = Bits.limitTo8Bits(value)

    @property
    def BCPrim(self):
        return (self.regsPri[B] << 8) + self.regsPri[C]

    @BCPrim.setter
    def BCPrim(self, value):
        value = Bits.limitTo16Bits(value)
        self.regsPri[B] = value >> 8
        self.regsPri[C] = Bits.limitTo8Bits(value)

    @property
    def AF(self):
        return (self.regs[A] << 8) + self.regs[F]

    @AF.setter
    def AF(self, value):
        value = Bits.limitTo16Bits(value)
        self.regs[A] = value >> 8
        self.regs[F] = Bits.limitTo8Bits(value)

    @property
    def AFPrim(self):
        return (self.regsPri[A] << 8) + self.regsPri[F]

    @AFPrim.setter
    def AFPrim(self, value):
        value = Bits.limitTo16Bits(value)
        self.regsPri[A] = value >> 8
        self.regsPri[F] = Bits.limitTo8Bits(value)

    @property
    def SP(self):
        return self.sp

    @SP.setter
    def SP(self, value):
        self.sp = Bits.limitTo16Bits(value)

    @property
    def I(self):
        return self.i

    @I.setter
    def I(self, value):
        self.i = Bits.limitTo8Bits(value)

    @property
    def IX(self):
        return self.ix

    @IX.setter
    def IX(self, value):
        self.ix = Bits.limitTo16Bits(value)

    @property
    def IY(self):
        return self.iy

    @IY.setter
    def IY(self, value):
        self.iy = Bits.limitTo16Bits(value)

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
                 debugger=EmptyDebugger(),
                 display=None):

        self.logger = logger
        self.debugger = debugger
        self.display = display

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

    def _dispatchDDCB(self, cpu, opcode, logger):
        pc = self.PC  # consume displacement byte (auto-increments)
        displacement = cpu.ram[pc]
        fourthbyte = cpu.ram[cpu.PC]  # consume operation byte
        fullOpcode = (opcode << 16) + (displacement << 8) + fourthbyte
        handler = self.ddcbTable[fourthbyte]
        if handler is None:
            self._missingOpcode(pc, fullOpcode)
            return
        self.debugger.next_opcode(pc, self)
        handler(self, fullOpcode, self.logger)

    def _dispatchFDCB(self, cpu, opcode, logger):
        pc = self.PC  # consume displacement byte (auto-increments)
        displacement = cpu.ram[pc]
        fourthbyte = cpu.ram[cpu.PC]  # consume operation byte
        fullOpcode = (opcode << 16) + (displacement << 8) + fourthbyte
        handler = self.fdcbTable[fourthbyte]
        if handler is None:
            self._missingOpcode(pc, fullOpcode)
            return
        self.debugger.next_opcode(pc, self)
        handler(self, fullOpcode, self.logger)

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

    def _checkTimers(self):
        if self.display and self.tstates >= 69888:
            self.tstates -= 69888
            self._interruptPending = True
            self.display.update(self.ram)
            self._frame_count = getattr(self, '_frame_count', 0) + 1
            if self._frame_count % 50 == 0:
                print("PC=0x{:04X} iff1={} im={} IY=0x{:04X}".format(
                    self.pc, self.iff1, self.im, self.IY))

    def run(self, pc=0x0):
        self.pc = pc
        while True:
            if not self.halted:
                self.readOp()
            else:
                self.m_cycles, self.t_states = 1, 4
            self._checkInterrupts()
            self._checkTimers()
