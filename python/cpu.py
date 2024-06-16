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
        self.pc += 1
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

        self.dispatchTable = {
            0x00: Opcodes.nop,
            0x01: Opcodes.ld16,
            0x02: Opcodes.ld_bc_a,
            0x03: Opcodes.inc16,
            0x04: Opcodes.inc8,
            0x05: Opcodes.dec8b,
            0x06: Opcodes.ld8n,
            0x07: Opcodes.rlca,
            0x08: Opcodes.ex_af_afprim,
            0x09: Opcodes.add16,
            0x0a: Opcodes.ld_a_bc,
            0x0b: Opcodes.dec16b,
            0x0c: Opcodes.inc8,
            0x0d: Opcodes.dec8b,
            0x0e: Opcodes.ld8n,
            0x0f: Opcodes.rrca,
            0x10: Opcodes.djnz,
            0x11: Opcodes.ld16,
            0x12: Opcodes.ld_de_a,
            0x13: Opcodes.inc16,
            0x14: Opcodes.inc8,
            0x15: Opcodes.dec8b,
            0x16: Opcodes.ld8n,
            0x17: Opcodes.lra,
            0x18: Opcodes.jr_e,
            0x19: Opcodes.add16,
            0x1a: Opcodes.ld_a_de,
            0x1b: Opcodes.dec16b,
            0x1c: Opcodes.inc8,
            0x1d: Opcodes.dec8b,
            0x1e: Opcodes.ld8n,
            0x1f: Opcodes.rra,
            0x20: Opcodes.jpnz,
            0x21: Opcodes.ld16,
            0x22: Opcodes.ldNnHl,
            0x23: Opcodes.inc16,
            0x24: Opcodes.inc8,
            0x25: Opcodes.dec8b,
            0x26: Opcodes.ld8n,
            0x27: Opcodes.daa,
            0x28: Opcodes.jrz,
            0x29: Opcodes.add16,
            0x2a: Opcodes.ldHl_addr,
            0x2b: Opcodes.dec16b,
            0x2c: Opcodes.inc8,
            0x2d: Opcodes.dec8b,
            0x2e: Opcodes.ld8n,
            0x2f: Opcodes.cpl,
            0x30: Opcodes.jpnc,
            0x31: Opcodes.ld16,
            0x32: Opcodes.ldnn_a,
            0x33: Opcodes.inc16,
            0x34: Opcodes.inc_at_hl,
            0x35: Opcodes.dec_at_hl,
            0x36: Opcodes.ld_addr,
            0x37: Opcodes.scf,
            0x38: Opcodes.jr_c,
            0x39: Opcodes.add16,
            0x3a: Opcodes.ld_a_nn,
            0x3b: Opcodes.dec16b,
            0x3c: Opcodes.inc8,
            0x3d: Opcodes.dec8b,
            0x3e: Opcodes.ld8n,
            0x3f: Opcodes.ccf,
            0x40: Opcodes.ld8,
            0x41: Opcodes.ld8,
            0x42: Opcodes.ld8,
            0x43: Opcodes.ld8,
            0x44: Opcodes.ld8,
            0x45: Opcodes.ld8,
            0x46: Opcodes.ld_r_hl,
            0x47: Opcodes.ld8,
            0x48: Opcodes.ld8,
            0x49: Opcodes.ld8,
            0x4a: Opcodes.ld8,
            0x4b: Opcodes.ld8,
            0x4c: Opcodes.ld8,
            0x4d: Opcodes.ld8,
            0x4e: Opcodes.ld_r_hl,
            0x4f: Opcodes.ld8,
            0x50: Opcodes.ld8,
            0x51: Opcodes.ld8,
            0x52: Opcodes.ld8,
            0x53: Opcodes.ld8,
            0x54: Opcodes.ld8,
            0x55: Opcodes.ld8,
            0x56: Opcodes.ld_r_hl,
            0x57: Opcodes.ld8,
            0x58: Opcodes.ld8,
            0x59: Opcodes.ld8,
            0x5a: Opcodes.ld8,
            0x5b: Opcodes.ld8,
            0x5c: Opcodes.ld8,
            0x5d: Opcodes.ld8,
            0x5e: Opcodes.ld_r_hl,
            0x5f: Opcodes.ld8,
            0x60: Opcodes.ld8,
            0x61: Opcodes.ld8,
            0x62: Opcodes.ld8,
            0x63: Opcodes.ld8,
            0x64: Opcodes.ld8,
            0x65: Opcodes.ld8,
            0x66: Opcodes.ld_r_hl,
            0x67: Opcodes.ld8,
            0x68: Opcodes.ld8,
            0x69: Opcodes.ld8,
            0x6a: Opcodes.ld8,
            0x6b: Opcodes.ld8,
            0x6c: Opcodes.ld8,
            0x6d: Opcodes.ld8,
            0x6e: Opcodes.ld_r_hl,
            0x6f: Opcodes.ld8,
            0x70: Opcodes.ldhlr,
            0x71: Opcodes.ldhlr,
            0x72: Opcodes.ldhlr,
            0x73: Opcodes.ldhlr,
            0x74: Opcodes.ldhlr,
            0x75: Opcodes.ldhlr,
            0x76: Opcodes.hlt,
            0x77: Opcodes.ldhlr,
            0x78: Opcodes.ld8,
            0x79: Opcodes.ld8,
            0x7a: Opcodes.ld8,
            0x7b: Opcodes.ld8,
            0x7c: Opcodes.ld8,
            0x7d: Opcodes.ld8,
            0x7e: Opcodes.ld_r_hl,
            0x7f: Opcodes.ld8,
            0x80: Opcodes.add_r,
            0x81: Opcodes.add_r,
            0x82: Opcodes.add_r,
            0x83: Opcodes.add_r,
            0x84: Opcodes.add_r,
            0x85: Opcodes.add_r,
            0x86: Opcodes.add_a_hl,
            0x87: Opcodes.add_r,
            0x88: Opcodes.adc_r,
            0x89: Opcodes.adc_r,
            0x8a: Opcodes.adc_r,
            0x8b: Opcodes.adc_r,
            0x8c: Opcodes.adc_r,
            0x8d: Opcodes.adc_r,
            0x8e: Opcodes.adc_a_hl,
            0x8f: Opcodes.adc_r,
            0x90: Opcodes.sub_r,
            0x91: Opcodes.sub_r,
            0x92: Opcodes.sub_r,
            0x93: Opcodes.sub_r,
            0x94: Opcodes.sub_r,
            0x95: Opcodes.sub_r,
            0x96: Opcodes.sub_a_hl,
            0x97: Opcodes.sub_r,
            0x98: Opcodes.sbc_r,
            0x99: Opcodes.sbc_r,
            0x9a: Opcodes.sbc_r,
            0x9b: Opcodes.sbc_r,
            0x9c: Opcodes.sbc_r,
            0x9d: Opcodes.sbc_r,
            0x9e: Opcodes.sbc_hl,
            0x9f: Opcodes.sbc_r,
            0xa0: Opcodes._and,
            0xa1: Opcodes._and,
            0xa2: Opcodes._and,
            0xa3: Opcodes._and,
            0xa4: Opcodes._and,
            0xa5: Opcodes._and,
            0xa6: Opcodes._and_hl,
            0xa7: Opcodes._and,
            0xa8: Opcodes.xorA,
            0xa9: Opcodes.xorA,
            0xaa: Opcodes.xorA,
            0xab: Opcodes.xorA,
            0xac: Opcodes.xorA,
            0xad: Opcodes.xorA,
            0xae: Opcodes.xor_hl,
            0xaf: Opcodes.xorA,
            0xb0: Opcodes._or,
            0xb1: Opcodes._or,
            0xb2: Opcodes._or,
            0xb3: Opcodes._or,
            0xb4: Opcodes._or,
            0xb5: Opcodes._or,
            0xb6: Opcodes._or_hl,
            0xb7: Opcodes._or,
            0xb8: Opcodes.cp,
            0xb9: Opcodes.cp,
            0xba: Opcodes.cp,
            0xbb: Opcodes.cp,
            0xbc: Opcodes.cp,
            0xbd: Opcodes.cp,
            0xbe: Opcodes.cp_hl,
            0xbf: Opcodes.cp,
            0xc0: Opcodes.ret_cc,
            0xc1: Opcodes.pop,
            0xc2: Opcodes.jp_cond,
            0xc3: Opcodes.jp,
            0xc4: Opcodes.call_cond,
            0xc5: Opcodes.push,
            0xc6: Opcodes.add_r_n,
            0xc7: Opcodes.rst,
            0xc8: Opcodes.ret_cc,
            0xc9: Opcodes.ret,
            0xca: Opcodes.jp_cond,
            0xcb: [self.twoBytesOpcodes],
            0xcc: Opcodes.call_cond,
            0xcd: Opcodes.call,
            0xce: Opcodes.adc_n,
            0xcf: Opcodes.rst,
            0xd0: Opcodes.ret_cc,
            0xd1: Opcodes.pop,
            0xd2: Opcodes.jp_cond,
            0xd3: Opcodes.out,
            0xd4: Opcodes.call_cond,
            0xd5: Opcodes.push,
            0xd6: Opcodes.sub_n,
            0xd7: Opcodes.rst,
            0xd8: Opcodes.ret_cc,
            0xd9: Opcodes.exx,
            0xda: Opcodes.jp_cond,
            0xdb: Opcodes.in_a_n,
            0xdc: Opcodes.call_cond,
            0xdd: [self.twoBytesOpcodes],
            0xde: Opcodes.sbc_n,
            0xdf: Opcodes.rst,
            0xe0: Opcodes.ret_cc,
            0xe1: Opcodes.pop,
            0xe2: Opcodes.jp_cond,
            0xe4: Opcodes.call_cond,
            0xe5: Opcodes.push,
            0xe6: Opcodes.and_n,
            0xe7: Opcodes.rst,
            0xe8: Opcodes.ret_cc,
            0xe9: Opcodes.jp_hl,
            0xea: Opcodes.jp_cond,
            0xeb: Opcodes.ex_de_hl,
            0xec: Opcodes.call_cond,
            0xed: [self.twoBytesOpcodes],
            0xee: Opcodes.xor_n,
            0xef: Opcodes.rst,
            0xf0: Opcodes.ret_cc,
            0xf1: Opcodes.pop,
            0xf2: Opcodes.jp_cond,
            0xf3: Opcodes.disableInterrupts,
            0xf4: Opcodes.call_cond,
            0xf5: Opcodes.push,
            0xf6: Opcodes.or_n,
            0xf7: Opcodes.rst,
            0xf8: Opcodes.ret_cc,
            0xf9: Opcodes.ld_sp_hl,
            0xfa: Opcodes.jp_cond,
            0xfb: Opcodes.enableInterrupts,
            0xfc: Opcodes.call_cond,
            0xfd: [self.twoBytesOpcodes],
            0xfe: Opcodes.cp_n,
            0xff: Opcodes.rst,
            0xcb00: Opcodes.rlc_n,
            0xcb01: Opcodes.rlc_n,
            0xcb02: Opcodes.rlc_n,
            0xcb03: Opcodes.rlc_n,
            0xcb04: Opcodes.rlc_n,
            0xcb05: Opcodes.rlc_n,
            0xcb06: Opcodes.rlc_at_hl,
            0xcb07: Opcodes.rlc_n,
            0xcb08: Opcodes.rrc_n,
            0xcb09: Opcodes.rrc_n,
            0xcb0a: Opcodes.rrc_n,
            0xcb0b: Opcodes.rrc_n,
            0xcb0c: Opcodes.rrc_n,
            0xcb0d: Opcodes.rrc_n,
            0xcb0e: Opcodes.rrc_at_hl,
            0xcb0f: Opcodes.rrc_n,
            0xcb10: Opcodes.rl_n,
            0xcb11: Opcodes.rl_n,
            0xcb12: Opcodes.rl_n,
            0xcb13: Opcodes.rl_n,
            0xcb14: Opcodes.rl_n,
            0xcb15: Opcodes.rl_n,
            0xcb16: Opcodes.rl_at_hl,
            0xcb17: Opcodes.rl_n,
            0xcb18: Opcodes.rr_n,
            0xcb19: Opcodes.rr_n,
            0xcb1a: Opcodes.rr_n,
            0xcb1b: Opcodes.rr_n,
            0xcb1c: Opcodes.rr_n,
            0xcb1d: Opcodes.rr_n,
            0xcb1e: Opcodes.rr_at_hl,
            0xcb1f: Opcodes.rr_n,
            0xcb20: Opcodes.sla_n,
            0xcb21: Opcodes.sla_n,
            0xcb22: Opcodes.sla_n,
            0xcb23: Opcodes.sla_n,
            0xcb24: Opcodes.sla_n,
            0xcb25: Opcodes.sla_n,
            0xcb26: Opcodes.sla_at_hl,
            0xcb27: Opcodes.sla_n,
            0xcb28: Opcodes.sra_n,
            0xcb29: Opcodes.sra_n,
            0xcb2a: Opcodes.sra_n,
            0xcb2b: Opcodes.sra_n,
            0xcb2c: Opcodes.sra_n,
            0xcb2d: Opcodes.sra_n,
            0xcb2e: Opcodes.sra_at_hl,
            0xcb2f: Opcodes.sra_n,
            0xcb30: Opcodes.sll_n,
            0xcb31: Opcodes.sll_n,
            0xcb32: Opcodes.sll_n,
            0xcb33: Opcodes.sll_n,
            0xcb34: Opcodes.sll_n,
            0xcb35: Opcodes.sll_n,
            0xcb36: Opcodes.sll_at_hl,
            0xcb37: Opcodes.sll_n,
            0xcb38: Opcodes.srl_r,
            0xcb39: Opcodes.srl_r,
            0xcb3a: Opcodes.srl_r,
            0xcb3b: Opcodes.srl_r,
            0xcb3c: Opcodes.srl_r,
            0xcb3d: Opcodes.srl_r,
            0xcb3e: Opcodes.srl_at_hl,
            0xcb3f: Opcodes.srl_r,
            0xcb40: Opcodes.bit_r_n,
            0xcb41: Opcodes.bit_r_n,
            0xcb42: Opcodes.bit_r_n,
            0xcb43: Opcodes.bit_r_n,
            0xcb44: Opcodes.bit_r_n,
            0xcb45: Opcodes.bit_r_n,
            0xcb46: Opcodes.bit_r_at_hl,
            0xcb47: Opcodes.bit_r_n,
            0xcb48: Opcodes.bit_r_n,
            0xcb49: Opcodes.bit_r_n,
            0xcb4a: Opcodes.bit_r_n,
            0xcb4b: Opcodes.bit_r_n,
            0xcb4c: Opcodes.bit_r_n,
            0xcb4d: Opcodes.bit_r_n,
            0xcb4e: Opcodes.bit_r_at_hl,
            0xcb4f: Opcodes.bit_r_n,
            0xcb50: Opcodes.bit_r_n,
            0xcb51: Opcodes.bit_r_n,
            0xcb52: Opcodes.bit_r_n,
            0xcb53: Opcodes.bit_r_n,
            0xcb54: Opcodes.bit_r_n,
            0xcb55: Opcodes.bit_r_n,
            0xcb56: Opcodes.bit_r_at_hl,
            0xcb57: Opcodes.bit_r_n,
            0xcb58: Opcodes.bit_r_n,
            0xcb59: Opcodes.bit_r_n,
            0xcb5a: Opcodes.bit_r_n,
            0xcb5b: Opcodes.bit_r_n,
            0xcb5c: Opcodes.bit_r_n,
            0xcb5d: Opcodes.bit_r_n,
            0xcb5e: Opcodes.bit_r_at_hl,
            0xcb5f: Opcodes.bit_r_n,
            0xcb60: Opcodes.bit_r_n,
            0xcb61: Opcodes.bit_r_n,
            0xcb62: Opcodes.bit_r_n,
            0xcb63: Opcodes.bit_r_n,
            0xcb64: Opcodes.bit_r_n,
            0xcb65: Opcodes.bit_r_n,
            0xcb66: Opcodes.bit_r_at_hl,
            0xcb67: Opcodes.bit_r_n,
            0xcb68: Opcodes.bit_r_n,
            0xcb69: Opcodes.bit_r_n,
            0xcb6a: Opcodes.bit_r_n,
            0xcb6b: Opcodes.bit_r_n,
            0xcb6c: Opcodes.bit_r_n,
            0xcb6d: Opcodes.bit_r_n,
            0xcb6e: Opcodes.bit_r_at_hl,
            0xcb6f: Opcodes.bit_r_n,
            0xcb70: Opcodes.bit_r_n,
            0xcb71: Opcodes.bit_r_n,
            0xcb72: Opcodes.bit_r_n,
            0xcb73: Opcodes.bit_r_n,
            0xcb74: Opcodes.bit_r_n,
            0xcb75: Opcodes.bit_r_n,
            0xcb76: Opcodes.bit_r_at_hl,
            0xcb77: Opcodes.bit_r_n,
            0xcb78: Opcodes.bit_r_n,
            0xcb79: Opcodes.bit_r_n,
            0xcb7a: Opcodes.bit_r_n,
            0xcb7b: Opcodes.bit_r_n,
            0xcb7c: Opcodes.bit_r_n,
            0xcb7d: Opcodes.bit_r_n,
            0xcb7e: Opcodes.bit_r_at_hl,
            0xcb7f: Opcodes.bit_r_n,
            0xcb80: Opcodes.res_r_n,
            0xcb81: Opcodes.res_r_n,
            0xcb82: Opcodes.res_r_n,
            0xcb83: Opcodes.res_r_n,
            0xcb84: Opcodes.res_r_n,
            0xcb85: Opcodes.res_r_n,
            0xcb86: Opcodes.res_r_at_hl,
            0xcb87: Opcodes.res_r_n,
            0xcb88: Opcodes.res_r_n,
            0xcb89: Opcodes.res_r_n,
            0xcb8a: Opcodes.res_r_n,
            0xcb8b: Opcodes.res_r_n,
            0xcb8c: Opcodes.res_r_n,
            0xcb8d: Opcodes.res_r_n,
            0xcb8e: Opcodes.res_r_at_hl,
            0xcb8f: Opcodes.res_r_n,
            0xcb90: Opcodes.res_r_n,
            0xcb91: Opcodes.res_r_n,
            0xcb92: Opcodes.res_r_n,
            0xcb93: Opcodes.res_r_n,
            0xcb94: Opcodes.res_r_n,
            0xcb95: Opcodes.res_r_n,
            0xcb96: Opcodes.res_r_at_hl,
            0xcb97: Opcodes.res_r_n,
            0xcb98: Opcodes.res_r_n,
            0xcb99: Opcodes.res_r_n,
            0xcb9a: Opcodes.res_r_n,
            0xcb9b: Opcodes.res_r_n,
            0xcb9c: Opcodes.res_r_n,
            0xcb9d: Opcodes.res_r_n,
            0xcb9e: Opcodes.res_r_at_hl,
            0xcb9f: Opcodes.res_r_n,
            0xcba0: Opcodes.res_r_n,
            0xcba1: Opcodes.res_r_n,
            0xcba2: Opcodes.res_r_n,
            0xcba3: Opcodes.res_r_n,
            0xcba4: Opcodes.res_r_n,
            0xcba5: Opcodes.res_r_n,
            0xcba6: Opcodes.res_r_at_hl,
            0xcba7: Opcodes.res_r_n,
            0xcba8: Opcodes.res_r_n,
            0xcba9: Opcodes.res_r_n,
            0xcbaa: Opcodes.res_r_n,
            0xcbab: Opcodes.res_r_n,
            0xcbac: Opcodes.res_r_n,
            0xcbad: Opcodes.res_r_n,
            0xcbae: Opcodes.res_r_at_hl,
            0xcbaf: Opcodes.res_r_n,
            0xcbb0: Opcodes.res_r_n,
            0xcbb1: Opcodes.res_r_n,
            0xcbb2: Opcodes.res_r_n,
            0xcbb3: Opcodes.res_r_n,
            0xcbb4: Opcodes.res_r_n,
            0xcbb5: Opcodes.res_r_n,
            0xcbb6: Opcodes.res_r_at_hl,
            0xcbb7: Opcodes.res_r_n,
            0xcbb8: Opcodes.res_r_n,
            0xcbb9: Opcodes.res_r_n,
            0xcbba: Opcodes.res_r_n,
            0xcbbb: Opcodes.res_r_n,
            0xcbbc: Opcodes.res_r_n,
            0xcbbd: Opcodes.res_r_n,
            0xcbbe: Opcodes.res_r_at_hl,
            0xcbbf: Opcodes.res_r_n,
            0xcbc0: Opcodes.set_r_n,
            0xcbc1: Opcodes.set_r_n,
            0xcbc2: Opcodes.set_r_n,
            0xcbc3: Opcodes.set_r_n,
            0xcbc4: Opcodes.set_r_n,
            0xcbc5: Opcodes.set_r_n,
            0xcbc6: Opcodes.set_r_at_hl,
            0xcbc7: Opcodes.set_r_n,
            0xcbc8: Opcodes.set_r_n,
            0xcbc9: Opcodes.set_r_n,
            0xcbca: Opcodes.set_r_n,
            0xcbcb: Opcodes.set_r_n,
            0xcbcc: Opcodes.set_r_n,
            0xcbcd: Opcodes.set_r_n,
            0xcbce: Opcodes.set_r_at_hl,
            0xcbcf: Opcodes.set_r_n,
            0xcbd0: Opcodes.set_r_n,
            0xcbd1: Opcodes.set_r_n,
            0xcbd2: Opcodes.set_r_n,
            0xcbd3: Opcodes.set_r_n,
            0xcbd4: Opcodes.set_r_n,
            0xcbd5: Opcodes.set_r_n,
            0xcbd6: Opcodes.set_r_at_hl,
            0xcbd7: Opcodes.set_r_n,
            0xcbd8: Opcodes.set_r_n,
            0xcbd9: Opcodes.set_r_n,
            0xcbda: Opcodes.set_r_n,
            0xcbdb: Opcodes.set_r_n,
            0xcbdc: Opcodes.set_r_n,
            0xcbdd: Opcodes.set_r_n,
            0xcbde: Opcodes.set_r_at_hl,
            0xcbdf: Opcodes.set_r_n,
            0xcbe0: Opcodes.set_r_n,
            0xcbe1: Opcodes.set_r_n,
            0xcbe2: Opcodes.set_r_n,
            0xcbe3: Opcodes.set_r_n,
            0xcbe4: Opcodes.set_r_n,
            0xcbe5: Opcodes.set_r_n,
            0xcbe6: Opcodes.set_r_at_hl,
            0xcbe7: Opcodes.set_r_n,
            0xcbe8: Opcodes.set_r_n,
            0xcbe9: Opcodes.set_r_n,
            0xcbea: Opcodes.set_r_n,
            0xcbeb: Opcodes.set_r_n,
            0xcbec: Opcodes.set_r_n,
            0xcbed: Opcodes.set_r_n,
            0xcbee: Opcodes.set_r_at_hl,
            0xcbef: Opcodes.set_r_n,
            0xcbf0: Opcodes.set_r_n,
            0xcbf1: Opcodes.set_r_n,
            0xcbf2: Opcodes.set_r_n,
            0xcbf3: Opcodes.set_r_n,
            0xcbf4: Opcodes.set_r_n,
            0xcbf5: Opcodes.set_r_n,
            0xcbf6: Opcodes.set_r_at_hl,
            0xcbf7: Opcodes.set_r_n,
            0xcbf8: Opcodes.set_r_n,
            0xcbf9: Opcodes.set_r_n,
            0xcbfa: Opcodes.set_r_n,
            0xcbfb: Opcodes.set_r_n,
            0xcbfc: Opcodes.set_r_n,
            0xcbfd: Opcodes.set_r_n,
            0xcbfe: Opcodes.set_r_at_hl,
            0xcbff: Opcodes.set_r_n,
            0xdd09: Opcodes.add_ix_rr,
            0xdd19: Opcodes.add_ix_rr,
            0xdd21: Opcodes.ld_ix_nn,
            0xdd22: Opcodes.ld_nn_ix,
            0xdd23: Opcodes.inc_ix,
            0xdd24: Opcodes.inc_ixh,
            0xdd25: Opcodes.dec_ixh,
            0xdd26: Opcodes.ld_ixh_nn,
            0xdd29: Opcodes.add_ix_rr,
            0xdd2a: Opcodes.ld_ix_at_nn,
            0xdd2b: Opcodes.dec_ix,
            0xdd2c: Opcodes.inc_ixl,
            0xdd2d: Opcodes.dec_ixl,
            0xdd2e: Opcodes.ld_ixl_nn,
            0xdd34: Opcodes.inc_at_ix_d,
            0xdd35: Opcodes.dec_at_ix_d,
            0xdd36: Opcodes.ld_at_ix_d_nn,
            0xdd39: Opcodes.add_ix_rr,
            0xdd40: Opcodes.ld8, # fallback to regular instruction
            0xdd41: Opcodes.ld8, # fallback to regular instruction
            0xdd42: Opcodes.ld8, # fallback to regular instruction
            0xdd43: Opcodes.ld8, # fallback to regular instruction
            0xdd44: Opcodes.ld_r_ixh,
            0xdd45: Opcodes.ld_r_ixl,
            0xdd46: Opcodes.ld_r_ix_d,
            0xdd47: Opcodes.ld8, # fallback to regular instruction
            0xdd48: Opcodes.ld8, # fallback to regular instruction
            0xdd49: Opcodes.ld8, # fallback to regular instruction
            0xdd4a: Opcodes.ld8, # fallback to regular instruction
            0xdd4b: Opcodes.ld8, # fallback to regular instruction
            0xdd4c: Opcodes.ld_r_ixh,
            0xdd4d: Opcodes.ld_r_ixl,
            0xdd4e: Opcodes.ld_r_ix_d,
            0xdd4f: Opcodes.ld8, # fallback to regular instruction
            0xdd50: Opcodes.ld8, # fallback to regular instruction
            0xdd51: Opcodes.ld8, # fallback to regular instruction
            0xdd52: Opcodes.ld8, # fallback to regular instruction
            0xdd53: Opcodes.ld8, # fallback to regular instruction
            0xdd54: Opcodes.ld_r_ixh,
            0xdd55: Opcodes.ld_r_ixl,
            0xdd56: Opcodes.ld_r_ix_d,
            0xdd57: Opcodes.ld8, # fallback to regular instruction
            0xdd58: Opcodes.ld8, # fallback to regular instruction
            0xdd59: Opcodes.ld8, # fallback to regular instruction
            0xdd5a: Opcodes.ld8, # fallback to regular instruction
            0xdd5b: Opcodes.ld8, # fallback to regular instruction
            0xdd5c: Opcodes.ld_r_ixh,
            0xdd5d: Opcodes.ld_r_ixl,
            0xdd5e: Opcodes.ld_r_ix_d,
            0xdd5f: Opcodes.ld8, # fallback to regular instruction
            0xdd60: Opcodes.ld_ixh_r,
            0xdd61: Opcodes.ld_ixh_r,
            0xdd62: Opcodes.ld_ixh_r,
            0xdd63: Opcodes.ld_ixh_r,
            0xdd64: Opcodes.ld_ixh_r,
            0xdd65: Opcodes.ld_ixh_r,
            0xdd66: Opcodes.ld_r_ix_d,
            0xdd67: Opcodes.ld_ixh_r,
            0xdd68: Opcodes.ld_ixl_r,
            0xdd69: Opcodes.ld_ixl_r,
            0xdd6a: Opcodes.ld_ixl_r,
            0xdd6b: Opcodes.ld_ixl_r,
            0xdd6c: Opcodes.ld_ixl_ixh,
            0xdd6d: Opcodes.ld_ixl_r,
            0xdd6e: Opcodes.ld_r_ix_d,
            0xdd6f: Opcodes.ld_ixl_r,
            0xdd70: Opcodes.ld_at_ix_d_r,
            0xdd71: Opcodes.ld_at_ix_d_r,
            0xdd72: Opcodes.ld_at_ix_d_r,
            0xdd73: Opcodes.ld_at_ix_d_r,
            0xdd74: Opcodes.ld_at_ix_d_r,
            0xdd75: Opcodes.ld_at_ix_d_r,
            0xdd77: Opcodes.ld_at_ix_d_r,
            0xdd78: Opcodes.ld8, # fallback to regular instruction
            0xdd79: Opcodes.ld8, # fallback to regular instruction
            0xdd7a: Opcodes.ld8, # fallback to regular instruction
            0xdd7b: Opcodes.ld8, # fallback to regular instruction
            0xdd7c: Opcodes.ld8, # fallback to regular instruction
            0xdd7d: Opcodes.ld8, # fallback to regular instruction
            0xdd7e: Opcodes.ld_r_ix_d,
            0xdd7f: Opcodes.ld8, # fallback to regular instruction
            0xdda4: Opcodes.and_ixh,
            0xdda5: Opcodes.and_ixl,
            0xdda6: Opcodes.and_ix_d,
            0xddac: Opcodes.xor_ixh,
            0xddad: Opcodes.xor_ixl,
            0xddae: Opcodes.xor_ix_d,
            0xddb4: Opcodes.or_ixh,
            0xddb5: Opcodes.or_ixl,
            0xddb6: Opcodes.or_ix_d,
            0xddbc: Opcodes.cp_ixh,
            0xddbd: Opcodes.cp_ixl,
            0xddbe: Opcodes.cp_ix_d,
            0xdde1: Opcodes.pop_ix,
            0xdde5: Opcodes.push_ix,
            0xdde9: Opcodes.jp_ix,
            0xdd84: Opcodes.add_a_ixh,
            0xdd85: Opcodes.add_a_ixl,
            0xdd86: Opcodes.add_a_ix_d,
            0xdd8c: Opcodes.adc_a_ixh,
            0xdd8d: Opcodes.adc_a_ixl,
            0xdd8e: Opcodes.adc_a_ix_d,
            0xdd94: Opcodes.sub_ixh,
            0xdd95: Opcodes.sub_ixl,
            0xdd96: Opcodes.sub_ix_d,
            0xdd9c: Opcodes.sbc_a_ixh,
            0xdd9d: Opcodes.sbc_a_ixl,
            0xdd9e: Opcodes.sbc_a_ix_d,
            0xddcb: [self.fourBytesOpcodes],
            0xed42: Opcodes.sbc,
            0xed43: Opcodes.ldNnRr,
            0xed45: Opcodes.retn,
            0xed44: Opcodes.neg,
            0xed46: Opcodes.im0,
            0xed47: Opcodes.ldExt,
            0xed4a: Opcodes.add_Hl_rr_c,
            0xed4b: Opcodes.ld16_nn,
            0xed4f: Opcodes.ldra,
            0xed52: Opcodes.sbc,
            0xed53: Opcodes.ldNnRr,
            0xed55: Opcodes.retn,
            0xed56: Opcodes.im1,
            0xed5a: Opcodes.add_Hl_rr_c,
            0xed5b: Opcodes.ld16_nn,
            0xed5e: Opcodes.im2,
            0xed5f: Opcodes.ldar,
            0xed62: Opcodes.sbc,
            0xed63: Opcodes.ldNnRr,
            0xed65: Opcodes.retn,
            0xed67: Opcodes.rrd,
            0xed6a: Opcodes.add_Hl_rr_c,
            0xed6b: Opcodes.ld16_nn,
            0xed6f: Opcodes.rld,
            0xed72: Opcodes.sbc,
            0xed73: Opcodes.ldNnRr,
            0xed75: Opcodes.retn,
            0xed78: Opcodes.portIn,
            0xed7a: Opcodes.add_Hl_rr_c,
            0xed7b: Opcodes.ld16_nn,
            0xeda0: Opcodes.ldi,
            0xeda1: Opcodes.cpi,
            0xeda8: Opcodes.ldd,
            0xeda9: Opcodes.cpd,
            0xedb0: Opcodes.ldir,
            0xedb8: Opcodes.lddr,
            0xedb9: Opcodes.cpdr,
            0xedb1: Opcodes.cpir,
            0xfd09: Opcodes.add_iy_rr,
            0xfd19: Opcodes.add_iy_rr,
            0xfd21: Opcodes.ldiy,
            0xfd22: Opcodes.ld_nn_iy,
            0xfd23: Opcodes.inc_iy,
            0xfd26: Opcodes.ld_ihy_nn,
            0xfd29: Opcodes.add_iy_rr,
            0xfd2a: Opcodes.ld_iy_at_nn,
            0xfd2b: Opcodes.dec_iy,
            0xfd2e: Opcodes.ld_iyl_nn,
            0xfd34: Opcodes.inc_mem_at_iy,
            0xfd35: Opcodes.dec_mem_at_iy,
            0xfd36: Opcodes.ldiy_d_n,
            0xfd39: Opcodes.add_iy_rr,
            0xfd40: Opcodes.ld8, # fallback to regular instruction
            0xfd41: Opcodes.ld8, # fallback to regular instruction
            0xfd42: Opcodes.ld8, # fallback to regular instruction
            0xfd43: Opcodes.ld8, # fallback to regular instruction
            0xfd44: Opcodes.ld_r_iyh,
            0xfd45: Opcodes.ld_r_iyl,
            0xfd46: Opcodes.ld_r_iy_d,
            0xfd47: Opcodes.ld8, # fallback to regular instruction
            0xfd48: Opcodes.ld8, # fallback to regular instruction
            0xfd49: Opcodes.ld8, # fallback to regular instruction
            0xfd4a: Opcodes.ld8, # fallback to regular instruction
            0xfd4b: Opcodes.ld8, # fallback to regular instruction
            0xfd4c: Opcodes.ld_r_iyh,
            0xfd4d: Opcodes.ld_r_iyl,
            0xfd4e: Opcodes.ld_r_iy_d,
            0xfd4f: Opcodes.ld8, # fallback to regular instruction
            0xfd50: Opcodes.ld8, # fallback to regular instruction
            0xfd51: Opcodes.ld8, # fallback to regular instruction
            0xfd52: Opcodes.ld8, # fallback to regular instruction
            0xfd53: Opcodes.ld8, # fallback to regular instruction
            0xfd54: Opcodes.ld_r_iyh,
            0xfd55: Opcodes.ld_r_iyl,
            0xfd56: Opcodes.ld_r_iy_d,
            0xfd57: Opcodes.ld8, # fallback to regular instruction
            0xfd58: Opcodes.ld8, # fallback to regular instruction
            0xfd59: Opcodes.ld8, # fallback to regular instruction
            0xfd5a: Opcodes.ld8, # fallback to regular instruction
            0xfd5b: Opcodes.ld8, # fallback to regular instruction
            0xfd5c: Opcodes.ld_r_iyh,
            0xfd5d: Opcodes.ld_r_iyl,
            0xfd5e: Opcodes.ld_r_iy_d,
            0xfd5f: Opcodes.ld8, # fallback to regular instruction
            0xfd60: Opcodes.ld_iyh_r,
            0xfd61: Opcodes.ld_iyh_r,
            0xfd62: Opcodes.ld_iyh_r,
            0xfd63: Opcodes.ld_iyh_r,
            0xfd64: Opcodes.ld8, # fallback to regular instruction
            0xfd65: Opcodes.ld_iyh_r,
            0xfd66: Opcodes.ld_r_iy_d,
            0xfd67: Opcodes.ld_iyh_r,
            0xfd68: Opcodes.ld_iyl_r,
            0xfd69: Opcodes.ld_iyl_r,
            0xfd6a: Opcodes.ld_iyl_r,
            0xfd6b: Opcodes.ld_iyl_r,
            0xfd6c: Opcodes.ld_iyl_iyh, # fallback to regular instruction
            0xfd6d: Opcodes.ld_iyl_r,
            0xfd6e: Opcodes.ld_r_iy_d,
            0xfd6f: Opcodes.ld_iyl_r,
            0xfd70: Opcodes.ld_at_iy_d_r,
            0xfd71: Opcodes.ld_at_iy_d_r,
            0xfd72: Opcodes.ld_at_iy_d_r,
            0xfd73: Opcodes.ld_at_iy_d_r,
            0xfd74: Opcodes.ld_at_iy_d_r,
            0xfd75: Opcodes.ld_at_iy_d_r,
            0xfd77: Opcodes.ld_at_iy_d_r,
            0xfd78: Opcodes.ld8, # fallback to regular instruction
            0xfd79: Opcodes.ld8, # fallback to regular instruction
            0xfd7a: Opcodes.ld8, # fallback to regular instruction
            0xfd7b: Opcodes.ld8, # fallback to regular instruction
            0xfd7c: Opcodes.ld8, # fallback to regular instruction
            0xfd7d: Opcodes.ld8, # fallback to regular instruction
            0xfd7e: Opcodes.ld_r_iy_d,
            0xfd7f: Opcodes.ld8, # fallback to regular instruction
            0xfd84: Opcodes.add_a_iyh,
            0xfd85: Opcodes.add_a_iyl,
            0xfd86: Opcodes.add_a_iy_d,
            0xfd8c: Opcodes.adc_a_iyh,
            0xfd8d: Opcodes.adc_a_iyl,
            0xfd8e: Opcodes.adc_a_iy_d,
            0xfd94: Opcodes.sub_iyh,
            0xfd95: Opcodes.sub_iyl,
            0xfd96: Opcodes.sub_iy_d,
            0xfd9c: Opcodes.sbc_a_iyh,
            0xfd9d: Opcodes.sbc_a_iyl,
            0xfd9e: Opcodes.sbc_a_iy_d,
            0xfda4: Opcodes.and_iyh,
            0xfda5: Opcodes.and_iyl,
            0xfda6: Opcodes.and_iy_d,
            0xfdac: Opcodes.xor_iyh,
            0xfdad: Opcodes.xor_iyl,
            0xfdae: Opcodes.xor_iy_d,
            0xfdb4: Opcodes.or_iyh,
            0xfdb5: Opcodes.or_iyl,
            0xfdb6: Opcodes.or_iy_d,
            0xfdbc: Opcodes.cp_iyh,
            0xfdbd: Opcodes.cp_iyl,
            0xfdbe: Opcodes.cp_iy_d,
            0xfdcb: [self.fourBytesOpcodes],
            0xfde1: Opcodes.pop_iy,
            0xfde5: Opcodes.push_iy,
            0xfde9: Opcodes.jp_iy,
            0xddcb0106: Opcodes.rlc_at_ix_n,
            0xddcb010e: Opcodes.rrc_at_ix_n,
            0xddcb0116: Opcodes.rl_at_ix_n,
            0xddcb011e: Opcodes.rr_at_ix_n,
            0xddcb0126: Opcodes.sla_at_ix_n,
            0xddcb012e: Opcodes.sra_at_ix_n,
            0xddcb0136: Opcodes.sll_at_ix_n,
            0xddcb013e: Opcodes.srl_at_ix_n,
            0xddcb0146: Opcodes.bit_bit_ix,
            0xddcb014e: Opcodes.bit_bit_ix,
            0xddcb0156: Opcodes.bit_bit_ix,
            0xddcb015e: Opcodes.bit_bit_ix,
            0xddcb0166: Opcodes.bit_bit_ix,
            0xddcb016e: Opcodes.bit_bit_ix,
            0xddcb0176: Opcodes.bit_bit_ix,
            0xddcb017e: Opcodes.bit_bit_ix,
            0xddcb0186: Opcodes.bit_res_ix,
            0xddcb018e: Opcodes.bit_res_ix,
            0xddcb0196: Opcodes.bit_res_ix,
            0xddcb019e: Opcodes.bit_res_ix,
            0xddcb01a6: Opcodes.bit_res_ix,
            0xddcb01ae: Opcodes.bit_res_ix,
            0xddcb01b6: Opcodes.bit_res_ix,
            0xddcb01be: Opcodes.bit_res_ix,
            0xddcb01c6: Opcodes.bit_set_ix,
            0xddcb01ce: Opcodes.bit_set_ix,
            0xddcb01d6: Opcodes.bit_set_ix,
            0xddcb01de: Opcodes.bit_set_ix,
            0xddcb01e6: Opcodes.bit_set_ix,
            0xddcb01ee: Opcodes.bit_set_ix,
            0xddcb01f6: Opcodes.bit_set_ix,
            0xddcb01fe: Opcodes.bit_set_ix,
            0xfdcb0106: Opcodes.rlc_at_iy_n,
            0xfdcb010e: Opcodes.rrc_at_iy_n,
            0xfdcb0116: Opcodes.rl_at_iy_n,
            0xfdcb011e: Opcodes.rr_at_iy_n,
            0xfdcb0126: Opcodes.sla_at_iy_n,
            0xfdcb012e: Opcodes.sra_at_iy_n,
            0xfdcb0136: Opcodes.sll_at_iy_n,
            0xfdcb013e: Opcodes.srl_at_iy_n,
            0xfdcb0146: Opcodes.bit_bit_iy,
            0xfdcb3046: Opcodes.bit_bit_iy,
            0xfdcb014e: Opcodes.bit_bit_iy,
            0xfdcb0156: Opcodes.bit_bit_iy,
            0xfdcb015e: Opcodes.bit_bit_iy,
            0xfdcb0166: Opcodes.bit_bit_iy,
            0xfdcb016e: Opcodes.bit_bit_iy,
            0xfdcb0176: Opcodes.bit_bit_iy,
            0xfdcb017e: Opcodes.bit_bit_iy,
            0xfdcb0186: Opcodes.bit_res_iy,
            0xfdcb018e: Opcodes.bit_res_iy,
            0xfdcb0196: Opcodes.bit_res_ix,
            0xfdcb019e: Opcodes.bit_res_ix,
            0xfdcb01a6: Opcodes.bit_res_ix,
            0xfdcb01ae: Opcodes.bit_res_ix,
            0xfdcb01b6: Opcodes.bit_res_ix,
            0xfdcb01be: Opcodes.bit_res_ix,
            0xfdcb01c6: Opcodes.bit_set_iy,
            0xfdcb01ce: Opcodes.bit_set_iy,
            0xfdcb01d6: Opcodes.bit_set_iy,
            0xfdcb01de: Opcodes.bit_set_iy,
            0xfdcb01e6: Opcodes.bit_set_iy,
            0xfdcb01ee: Opcodes.bit_set_iy,
            0xfdcb01f6: Opcodes.bit_set_iy,
            0xfdcb01fe: Opcodes.bit_set_iy,
            0xfdcb0246: Opcodes.bit_bit_iy,
            0xfdcb0476: Opcodes.bit_bit_iy,
            0xfdcb3086: Opcodes.bit_res,
            0xfdcb308e: Opcodes.bit_res,
            0xfdcb30a6: Opcodes.bit_res
        }

    def generateInterrupt(self):
        self.generateInterrupt = True

    def readOp(self):
        self.prev_pc = self.PC
        pc = self.prev_pc
        opcode = self.ram[pc]
        self.dispatch(opcode, pc)

    def twoBytesOpcodes(self, cpu, opcode, logger):
        pc = self.PC
        secondOpByte = self.ram[pc]
        fullOpcode = (opcode << 8) + secondOpByte
        self.dispatch(fullOpcode, pc)

    def fourBytesOpcodes(self, cpu, opcode, logger):
        pc = self.PC
        thirdbyte = cpu.ram[pc]
        fourthbyte = cpu.ram[cpu.PC]
        fullOpcode = (opcode << 16) + (thirdbyte << 8) + fourthbyte
        self.dispatch(fullOpcode, pc)

    def dispatch(self, opcode, pc):
        try:
            _dispatch = self.dispatchTable[opcode]
            if type(_dispatch) is not list:
                handled = self.debugger.next_opcode(pc, self)
                if handled:
                    return
            else:
                _dispatch = _dispatch[0]
            _dispatch(self, opcode, self.logger)
        except (IndexError, KeyboardInterrupt) as e:
            self.debugger.stop(self)
        except KeyError as e:
            self.printError(pc, opcode)
            if self.debugger.stopOnError:
                self.debugger.stop(self)

    def printError(self, pc, opcode):
        print("Missing opcode key: {1:x}, PC = 0x{0:x}".format(pc, opcode))

    def _checkInterrupts(self):
        if self.iff1 and self.generateInterrupt:
            self.generateInterrupt = False
            self.halted = Bits.reset()
            self.iff1 = Bits.reset()
            self.iff2 = Bits.reset()
            self.ram[--self.SP] = Bits.limitTo8Bits(self.pc)
            self.ram[--self.SP] = self.pc >> 8
            self.R += 1
            if self.im == 0 or self.im == 1:
                self.PC = 0x0038

    def _checkTimers(self):
        pass

    def run(self, pc=0x0):
        self.pc = pc
        while True:
            if not self.halted:
                self.readOp()
            self._checkInterrupts()
            self._checkTimers()
