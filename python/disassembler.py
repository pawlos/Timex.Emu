# Z80 Disassembler

from bits import Bits

_REG8 = ['B', 'C', 'D', 'E', 'H', 'L', '(HL)', 'A']
_REG16 = ['BC', 'DE', 'HL', 'SP']
_REG16AF = ['BC', 'DE', 'HL', 'AF']
_ALU = ['ADD A,', 'ADC A,', 'SUB ', 'SBC A,', 'AND ', 'XOR ', 'OR ', 'CP ']
_CC = ['NZ', 'Z', 'NC', 'C', 'PO', 'PE', 'P', 'M']
_ROT = ['RLC', 'RRC', 'RL', 'RR', 'SLA', 'SRA', 'SLL', 'SRL']

_BASE = {
    0x00: 'NOP', 0x02: 'LD (BC),A', 0x07: 'RLCA', 0x08: "EX AF,AF'",
    0x0A: 'LD A,(BC)', 0x0F: 'RRCA', 0x12: 'LD (DE),A', 0x17: 'RLA',
    0x1A: 'LD A,(DE)', 0x1F: 'RRA', 0x27: 'DAA', 0x2F: 'CPL',
    0x37: 'SCF', 0x3F: 'CCF', 0x76: 'HALT',
    0xC9: 'RET', 0xD9: 'EXX', 0xE3: 'EX (SP),HL', 0xE9: 'JP (HL)',
    0xEB: 'EX DE,HL', 0xF3: 'DI', 0xF9: 'LD SP,HL', 0xFB: 'EI',
}

_ED = {
    0x40: 'IN B,(C)', 0x41: 'OUT (C),B', 0x42: 'SBC HL,BC', 0x43: 'LD (nn),BC',
    0x44: 'NEG', 0x45: 'RETN', 0x46: 'IM 0', 0x47: 'LD I,A',
    0x48: 'IN C,(C)', 0x49: 'OUT (C),C', 0x4A: 'ADC HL,BC', 0x4B: 'LD BC,(nn)',
    0x4D: 'RETI', 0x4F: 'LD R,A',
    0x50: 'IN D,(C)', 0x51: 'OUT (C),D', 0x52: 'SBC HL,DE', 0x53: 'LD (nn),DE',
    0x56: 'IM 1', 0x57: 'LD A,I',
    0x58: 'IN E,(C)', 0x59: 'OUT (C),E', 0x5A: 'ADC HL,DE', 0x5B: 'LD DE,(nn)',
    0x5E: 'IM 2', 0x5F: 'LD A,R',
    0x60: 'IN H,(C)', 0x61: 'OUT (C),H', 0x62: 'SBC HL,HL', 0x63: 'LD (nn),HL',
    0x67: 'RRD',
    0x68: 'IN L,(C)', 0x69: 'OUT (C),L', 0x6A: 'ADC HL,HL', 0x6B: 'LD HL,(nn)',
    0x6F: 'RLD',
    0x72: 'SBC HL,SP', 0x73: 'LD (nn),SP',
    0x78: 'IN A,(C)', 0x79: 'OUT (C),A', 0x7A: 'ADC HL,SP', 0x7B: 'LD SP,(nn)',
    0xA0: 'LDI', 0xA1: 'CPI', 0xA2: 'INI', 0xA3: 'OUTI',
    0xA8: 'LDD', 0xA9: 'CPD', 0xAA: 'IND', 0xAB: 'OUTD',
    0xB0: 'LDIR', 0xB1: 'CPIR', 0xB2: 'INIR', 0xB3: 'OTIR',
    0xB8: 'LDDR', 0xB9: 'CPDR', 0xBA: 'INDR', 0xBB: 'OTDR',
}


class Disassembler:

    def decode(self, ram, addr):
        """Returns (mnemonic, byte_size) for instruction at addr."""
        op = ram[addr]

        # CB prefix: bit/rotate operations
        if op == 0xCB:
            return self._decode_cb(ram, addr)

        # DD/FD prefix: IX/IY operations
        if op in (0xDD, 0xFD):
            return self._decode_index(ram, addr, op)

        # ED prefix
        if op == 0xED:
            return self._decode_ed(ram, addr)

        # Base opcodes
        if op in _BASE:
            return _BASE[op], 1

        # LD r,r' (0x40-0x7F except 0x76)
        if 0x40 <= op <= 0x7F:
            return 'LD {},{}'.format(_REG8[(op >> 3) & 7], _REG8[op & 7]), 1

        # ALU r (0x80-0xBF)
        if 0x80 <= op <= 0xBF:
            return '{}{}'.format(_ALU[(op >> 3) & 7], _REG8[op & 7]), 1

        # LD r,n
        if op & 0xC7 == 0x06:
            n = ram[(addr + 1) & 0xFFFF]
            return 'LD {},{:02X}'.format(_REG8[(op >> 3) & 7], n), 2

        # LD rr,nn
        if op & 0xCF == 0x01:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'LD {},{:04X}'.format(_REG16[(op >> 4) & 3], nn), 3

        # INC/DEC r
        if op & 0xC7 == 0x04:
            return 'INC {}'.format(_REG8[(op >> 3) & 7]), 1
        if op & 0xC7 == 0x05:
            return 'DEC {}'.format(_REG8[(op >> 3) & 7]), 1

        # INC/DEC rr
        if op & 0xCF == 0x03:
            return 'INC {}'.format(_REG16[(op >> 4) & 3]), 1
        if op & 0xCF == 0x0B:
            return 'DEC {}'.format(_REG16[(op >> 4) & 3]), 1

        # ADD HL,rr
        if op & 0xCF == 0x09:
            return 'ADD HL,{}'.format(_REG16[(op >> 4) & 3]), 1

        # PUSH/POP
        if op & 0xCF == 0xC5:
            return 'PUSH {}'.format(_REG16AF[(op >> 4) & 3]), 1
        if op & 0xCF == 0xC1:
            return 'POP {}'.format(_REG16AF[(op >> 4) & 3]), 1

        # JP cc,nn
        if op & 0xC7 == 0xC2:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'JP {},{:04X}'.format(_CC[(op >> 3) & 7], nn), 3

        # CALL cc,nn
        if op & 0xC7 == 0xC4:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'CALL {},{:04X}'.format(_CC[(op >> 3) & 7], nn), 3

        # RET cc
        if op & 0xC7 == 0xC0:
            return 'RET {}'.format(_CC[(op >> 3) & 7]), 1

        # RST
        if op & 0xC7 == 0xC7:
            return 'RST {:02X}'.format(op & 0x38), 1

        # JP nn
        if op == 0xC3:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'JP {:04X}'.format(nn), 3

        # CALL nn
        if op == 0xCD:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'CALL {:04X}'.format(nn), 3

        # JR d
        if op == 0x18:
            d = Bits.from_twos_comp(ram[(addr + 1) & 0xFFFF])
            return 'JR {:04X}'.format((addr + 2 + d) & 0xFFFF), 2

        # JR cc,d
        if op in (0x20, 0x28, 0x30, 0x38):
            cc = {0x20: 'NZ', 0x28: 'Z', 0x30: 'NC', 0x38: 'C'}[op]
            d = Bits.from_twos_comp(ram[(addr + 1) & 0xFFFF])
            return 'JR {},{:04X}'.format(cc, (addr + 2 + d) & 0xFFFF), 2

        # DJNZ d
        if op == 0x10:
            d = Bits.from_twos_comp(ram[(addr + 1) & 0xFFFF])
            return 'DJNZ {:04X}'.format((addr + 2 + d) & 0xFFFF), 2

        # LD (nn),A / LD A,(nn)
        if op == 0x32:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'LD ({:04X}),A'.format(nn), 3
        if op == 0x3A:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'LD A,({:04X})'.format(nn), 3

        # LD (nn),HL / LD HL,(nn)
        if op == 0x22:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'LD ({:04X}),HL'.format(nn), 3
        if op == 0x2A:
            nn = ram[(addr + 1) & 0xFFFF] | (ram[(addr + 2) & 0xFFFF] << 8)
            return 'LD HL,({:04X})'.format(nn), 3

        # ALU n
        if op & 0xC7 == 0xC6:
            n = ram[(addr + 1) & 0xFFFF]
            return '{}{:02X}'.format(_ALU[(op >> 3) & 7], n), 2

        # OUT (n),A / IN A,(n)
        if op == 0xD3:
            return 'OUT ({:02X}),A'.format(ram[(addr + 1) & 0xFFFF]), 2
        if op == 0xDB:
            return 'IN A,({:02X})'.format(ram[(addr + 1) & 0xFFFF]), 2

        return '???', 1

    def _decode_cb(self, ram, addr):
        op = ram[(addr + 1) & 0xFFFF]
        r = _REG8[op & 7]
        if op < 0x40:
            return '{} {}'.format(_ROT[(op >> 3) & 7], r), 2
        elif op < 0x80:
            return 'BIT {},{}'.format((op >> 3) & 7, r), 2
        elif op < 0xC0:
            return 'RES {},{}'.format((op >> 3) & 7, r), 2
        else:
            return 'SET {},{}'.format((op >> 3) & 7, r), 2

    def _decode_index(self, ram, addr, prefix):
        ix = 'IX' if prefix == 0xDD else 'IY'
        op = ram[(addr + 1) & 0xFFFF]

        # IX/IY CB prefix
        if op == 0xCB:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            op2 = ram[(addr + 3) & 0xFFFF]
            sign = '+' if d >= 0 else ''
            disp = '{}{}' .format(sign, d)
            if op2 < 0x40:
                return '{} ({}{}){}'.format(_ROT[(op2 >> 3) & 7], ix, disp,
                    '' if (op2 & 7) == 6 else ','+_REG8[op2 & 7]), 4
            elif op2 < 0x80:
                return 'BIT {},({}{}){}'.format((op2 >> 3) & 7, ix, disp,
                    '' if (op2 & 7) == 6 else ','+_REG8[op2 & 7]), 4
            elif op2 < 0xC0:
                return 'RES {},({}{}){}'.format((op2 >> 3) & 7, ix, disp,
                    '' if (op2 & 7) == 6 else ','+_REG8[op2 & 7]), 4
            else:
                return 'SET {},({}{}){}'.format((op2 >> 3) & 7, ix, disp,
                    '' if (op2 & 7) == 6 else ','+_REG8[op2 & 7]), 4

        # ADD IX,rr
        if op & 0xCF == 0x09:
            rr = _REG16[(op >> 4) & 3]
            if rr == 'HL':
                rr = ix
            return 'ADD {},{}'.format(ix, rr), 2

        # LD IX,nn
        if op == 0x21:
            nn = ram[(addr + 2) & 0xFFFF] | (ram[(addr + 3) & 0xFFFF] << 8)
            return 'LD {},{:04X}'.format(ix, nn), 4

        # LD (nn),IX / LD IX,(nn)
        if op == 0x22:
            nn = ram[(addr + 2) & 0xFFFF] | (ram[(addr + 3) & 0xFFFF] << 8)
            return 'LD ({:04X}),{}'.format(nn, ix), 4
        if op == 0x2A:
            nn = ram[(addr + 2) & 0xFFFF] | (ram[(addr + 3) & 0xFFFF] << 8)
            return 'LD {},({:04X})'.format(ix, nn), 4

        # INC/DEC IX
        if op == 0x23:
            return 'INC {}'.format(ix), 2
        if op == 0x2B:
            return 'DEC {}'.format(ix), 2

        # PUSH/POP IX
        if op == 0xE5:
            return 'PUSH {}'.format(ix), 2
        if op == 0xE1:
            return 'POP {}'.format(ix), 2

        # EX (SP),IX
        if op == 0xE3:
            return 'EX (SP),{}'.format(ix), 2

        # JP (IX)
        if op == 0xE9:
            return 'JP ({})'.format(ix), 2

        # LD SP,IX
        if op == 0xF9:
            return 'LD SP,{}'.format(ix), 2

        # LD r,(IX+d) / LD (IX+d),r
        if op & 0xC7 == 0x46 and (op >> 3) & 7 != 6:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            sign = '+' if d >= 0 else ''
            return 'LD {},({}{}{})'  .format(_REG8[(op >> 3) & 7], ix, sign, d), 3
        if op & 0xF8 == 0x70 and op & 7 != 6:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            sign = '+' if d >= 0 else ''
            return 'LD ({}{}{}),{}'.format(ix, sign, d, _REG8[op & 7]), 3

        # LD (IX+d),n
        if op == 0x36:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            n = ram[(addr + 3) & 0xFFFF]
            sign = '+' if d >= 0 else ''
            return 'LD ({}{}{}),{:02X}'.format(ix, sign, d, n), 4

        # INC/DEC (IX+d)
        if op == 0x34:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            sign = '+' if d >= 0 else ''
            return 'INC ({}{}{})'.format(ix, sign, d), 3
        if op == 0x35:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            sign = '+' if d >= 0 else ''
            return 'DEC ({}{}{})'.format(ix, sign, d), 3

        # ALU (IX+d)
        if op & 0xC7 == 0x86:
            d = Bits.from_twos_comp(ram[(addr + 2) & 0xFFFF])
            sign = '+' if d >= 0 else ''
            return '{}({}{}{})'.format(_ALU[(op >> 3) & 7], ix, sign, d), 3

        # INC/DEC IXH/IXL
        if op == 0x24:
            return 'INC {}H'.format(ix), 2
        if op == 0x25:
            return 'DEC {}H'.format(ix), 2
        if op == 0x2C:
            return 'INC {}L'.format(ix), 2
        if op == 0x2D:
            return 'DEC {}L'.format(ix), 2

        # LD IXH/IXL,n
        if op == 0x26:
            return 'LD {}H,{:02X}'.format(ix, ram[(addr + 2) & 0xFFFF]), 3
        if op == 0x2E:
            return 'LD {}L,{:02X}'.format(ix, ram[(addr + 2) & 0xFFFF]), 3

        # Fallback: show raw bytes
        return '{} {:02X}'.format(ix, op), 2

    def _decode_ed(self, ram, addr):
        op = ram[(addr + 1) & 0xFFFF]
        if op in _ED:
            mnemonic = _ED[op]
            if 'nn' in mnemonic:
                nn = ram[(addr + 2) & 0xFFFF] | (ram[(addr + 3) & 0xFFFF] << 8)
                return mnemonic.replace('nn', '{:04X}'.format(nn)), 4
            return mnemonic, 2
        return 'ED {:02X}'.format(op), 2

    def disasm(self, ram, addr, count=8):
        for _ in range(count):
            mnemonic, size = self.decode(ram, addr)
            hexbytes = ' '.join('{:02X}'.format(ram[(addr + i) & 0xFFFF]) for i in range(size))
            print('{:04X}  {:<12s} {}'.format(addr, hexbytes, mnemonic))
            addr = (addr + size) & 0xFFFF
