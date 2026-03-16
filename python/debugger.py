#Z80 debugger
import sys
import re
from regs import ZF, SF, HF, PVF, NF, CF, A, B, C, D, E, H, L
from utility import Bits
from loggers import EmptyLogger, Logger

HOOK_ADDR_ALL = -1

class EmptyDebugger(object):
    def setBreakpoint(self, pc):
        pass

    def stop(self, cpu):
        pass

    def next_opcode(self, pc, cpu):
        pass


class Debugger(object):
    def __init__(self):
        self.isSingleStepping = False
        self.breakpoints = {}
        self.hooks = {}
        self.lastInput = ""
        self.stopOnError = True
        self.trace_buffer = []
        self.trace_enabled = False
        self.trace_size = 1000

    def setBreakpoint(self, pc):
        self.breakpoints[pc] = True

    def disableBreakpoint(self, pc):
        if pc in self.breakpoints:
            self.breakpoints[pc] = False

    def clearBreakpoint(self, pc):
        if pc in self.breakpoints:
            del self.breakpoints[pc]

    def setHook(self, pc, function):
        self.hooks[pc] = function

    def getAddr(self, input):
        return int(re.search('0x([0-9a-fA-F]+)$', input).group(1), base=16)

    def printBreakpoints(self):
        for pc in self.breakpoints:
            state = "active" if self.breakpoints[pc] else "inactive"
            print("Breakpoint at {:04X}, {}"
                  .format(pc, state))

    def attachDetachLogger(self, cpu):
        if type(cpu.logger) is not EmptyLogger:
            print("Detaching logger")
            cpu.logger = EmptyLogger()
        else:
            print("Attaching logger")
            cpu.logger = Logger(cpu)

    # Simple Z80 opcode name table for disassembly
    _OPCODES = {
        0x00:'NOP',0x01:'LD BC,nn',0x02:'LD (BC),A',0x03:'INC BC',0x04:'INC B',
        0x05:'DEC B',0x06:'LD B,n',0x07:'RLCA',0x08:"EX AF,AF'",0x09:'ADD HL,BC',
        0x0A:'LD A,(BC)',0x0B:'DEC BC',0x0C:'INC C',0x0D:'DEC C',0x0E:'LD C,n',
        0x0F:'RRCA',0x10:'DJNZ d',0x11:'LD DE,nn',0x12:'LD (DE),A',0x13:'INC DE',
        0x14:'INC D',0x15:'DEC D',0x16:'LD D,n',0x17:'RLA',0x18:'JR d',
        0x19:'ADD HL,DE',0x1A:'LD A,(DE)',0x1B:'DEC DE',0x1C:'INC E',0x1D:'DEC E',
        0x1E:'LD E,n',0x1F:'RRA',0x20:'JR NZ,d',0x21:'LD HL,nn',0x22:'LD (nn),HL',
        0x23:'INC HL',0x24:'INC H',0x25:'DEC H',0x26:'LD H,n',0x27:'DAA',
        0x28:'JR Z,d',0x29:'ADD HL,HL',0x2A:'LD HL,(nn)',0x2B:'DEC HL',0x2C:'INC L',
        0x2D:'DEC L',0x2E:'LD L,n',0x2F:'CPL',0x30:'JR NC,d',0x31:'LD SP,nn',
        0x32:'LD (nn),A',0x33:'INC SP',0x34:'INC (HL)',0x35:'DEC (HL)',
        0x36:'LD (HL),n',0x37:'SCF',0x38:'JR C,d',0x39:'ADD HL,SP',
        0x3A:'LD A,(nn)',0x3B:'DEC SP',0x3C:'INC A',0x3D:'DEC A',0x3E:'LD A,n',
        0x3F:'CCF',0x76:'HALT',
        0xC0:'RET NZ',0xC1:'POP BC',0xC2:'JP NZ,nn',0xC3:'JP nn',
        0xC4:'CALL NZ,nn',0xC5:'PUSH BC',0xC6:'ADD A,n',0xC7:'RST 00',
        0xC8:'RET Z',0xC9:'RET',0xCA:'JP Z,nn',0xCC:'CALL Z,nn',
        0xCD:'CALL nn',0xCE:'ADC A,n',0xCF:'RST 08',
        0xD0:'RET NC',0xD1:'POP DE',0xD2:'JP NC,nn',0xD3:'OUT (n),A',
        0xD4:'CALL NC,nn',0xD5:'PUSH DE',0xD6:'SUB n',0xD7:'RST 10',
        0xD8:'RET C',0xD9:'EXX',0xDA:'JP C,nn',0xDB:'IN A,(n)',
        0xDC:'CALL C,nn',0xDE:'SBC A,n',0xDF:'RST 18',
        0xE0:'RET PO',0xE1:'POP HL',0xE2:'JP PO,nn',0xE3:'EX (SP),HL',
        0xE4:'CALL PO,nn',0xE5:'PUSH HL',0xE6:'AND n',0xE7:'RST 20',
        0xE8:'RET PE',0xE9:'JP (HL)',0xEA:'JP PE,nn',0xEB:'EX DE,HL',
        0xEC:'CALL PE,nn',0xEE:'XOR n',0xEF:'RST 28',
        0xF0:'RET P',0xF1:'POP AF',0xF2:'JP P,nn',0xF3:'DI',
        0xF4:'CALL P,nn',0xF5:'PUSH AF',0xF6:'OR n',0xF7:'RST 30',
        0xF8:'RET M',0xF9:'LD SP,HL',0xFA:'JP M,nn',0xFB:'EI',
        0xFC:'CALL M,nn',0xFE:'CP n',0xFF:'RST 38',
    }
    _REG8 = ['B','C','D','E','H','L','(HL)','A']
    _ALU = ['ADD A,','ADC A,','SUB ','SBC A,','AND ','XOR ','OR ','CP ']

    def disasm_at(self, cpu, addr, count=8):
        for _ in range(count):
            op = cpu.ram[addr]
            if op in self._OPCODES:
                mnemonic = self._OPCODES[op]
                size = 1
                if 'nn' in mnemonic:
                    lo = cpu.ram[(addr+1) & 0xFFFF]
                    hi = cpu.ram[(addr+2) & 0xFFFF]
                    mnemonic = mnemonic.replace('nn', '{:04X}'.format((hi<<8)|lo))
                    size = 3
                elif 'n' in mnemonic:
                    mnemonic = mnemonic.replace('n', '{:02X}'.format(cpu.ram[(addr+1) & 0xFFFF]))
                    size = 2
                elif 'd' in mnemonic:
                    d = cpu.ram[(addr+1) & 0xFFFF]
                    offset = Bits.from_twos_comp(d)
                    target = (addr + 2 + offset) & 0xFFFF
                    mnemonic = mnemonic.replace('d', '{:04X}'.format(target))
                    size = 2
            elif 0x40 <= op <= 0x7F and op != 0x76:
                dst = self._REG8[(op >> 3) & 7]
                src = self._REG8[op & 7]
                mnemonic = 'LD {},{}'.format(dst, src)
                size = 1
            elif 0x80 <= op <= 0xBF:
                alu = self._ALU[(op >> 3) & 7]
                src = self._REG8[op & 7]
                mnemonic = '{}{}'.format(alu, src)
                size = 1
            elif op == 0xCB:
                mnemonic = 'CB {:02X}'.format(cpu.ram[(addr+1) & 0xFFFF])
                size = 2
            elif op in (0xDD, 0xFD):
                prefix = 'IX' if op == 0xDD else 'IY'
                mnemonic = '{} {:02X}'.format(prefix, cpu.ram[(addr+1) & 0xFFFF])
                size = 2
            elif op == 0xED:
                mnemonic = 'ED {:02X}'.format(cpu.ram[(addr+1) & 0xFFFF])
                size = 2
            else:
                mnemonic = '???'
                size = 1
            hexbytes = ' '.join('{:02X}'.format(cpu.ram[(addr+i) & 0xFFFF]) for i in range(size))
            print('{:04X}  {:<12s} {}'.format(addr, hexbytes, mnemonic))
            addr = (addr + size) & 0xFFFF

    def hexdump(self, cpu, addr, lines=8):
        for _ in range(lines):
            hexpart = ' '.join('{:02X}'.format(cpu.ram[(addr+i) & 0xFFFF]) for i in range(16))
            ascpart = ''.join(chr(cpu.ram[(addr+i) & 0xFFFF]) if 32 <= cpu.ram[(addr+i) & 0xFFFF] < 127 else '.' for i in range(16))
            print('{:04X}  {}  {}'.format(addr, hexpart, ascpart))
            addr = (addr + 16) & 0xFFFF

    def help(self):
        print("available commands")
        print("ir - print info about 8-bit registers")
        print("if - print info about flags")
        print("ir16 - print info about 16-bit registers")
        print("d [0x<addr>] - disassemble at addr (default: PC)")
        print("m 0x<addr> - hex dump memory at addr")
        print("pram 0x<addr> - print value from RAM at <addr>")
        print("b 0x<addr> - set a breakpoint at <addr>")
        print("bc 0x<addr> - clear a breakpoint at <addr>")
        print("bd 0x<addr> - disable a breakpoint at <addr>")
        print("bl - list all breakpoints")
        print("stack [n] - show n stack entries (default 8)")
        print("trace on/off - enable/disable execution trace")
        print("trace [n] - show last n traced instructions (default 20)")
        print("log - attach/detach logger")
        print("s - single step")
        print("c - continue")
        print("t - print timing info (m-cycles, t-states)")
        print("? - this help")
        print("exit/q - stop the program")

    def state(self, flag, flag_bit, flag_name):
        state = Bits.getNthBit(flag, flag_bit)
        return flag_name if state != 0 else flag_name.lower()

    def print16bitregs(self, cpu):
        print("AF : {:04X} "
              "BC : {:04X} "
              "DE : {:04X} "
              "HL : {:04X} "
              "IX : {:04X} "
              "IY : {:04X} "
              "SP : {:04X}"
              .format(cpu.AF, cpu.BC, cpu.DE, cpu.HL, cpu.IX, cpu.IY, cpu.SP))

    def print16bitregsprim(self, cpu):
        print("AF': {:04X} "
              "BC': {:04X} "
              "DE': {:04X} "
              "HL': {:04X}"
              .format(cpu.AFPrim, cpu.BCPrim, cpu.DEPrim, cpu.HLPrim))

    def print8bitregs(self, cpu):
        print("A : {:02X} "
              "B : {:02X} "
              "C : {:02X} "
              "D : {:02X} "
              "E : {:02X} "
              "H : {:02X} "
              "L : {:02X}"
              .format(cpu.regs[A], cpu.regs[B], cpu.regs[C], cpu.regs[D],
                      cpu.regs[E], cpu.regs[H], cpu.regs[L]))

    def print8bitregsprim(self, cpu):
        print("A': {:02X} "
              "B': {:02X} "
              "C': {:02X} "
              "D': {:02X} "
              "E': {:02X} "
              "H': {:02X} "
              "L': {:02X}"
              .format(cpu.regsPri[A], cpu.regsPri[B], cpu.regsPri[C],
                      cpu.regsPri[D], cpu.regsPri[E], cpu.regsPri[H],
                      cpu.regsPri[L]))

    def printflags(self, cpu):
        print("{} {} _ "
              "{} _ {} "
              "{} {}"
              .format(self.state(cpu.F, SF, "S"),
                      self.state(cpu.F, ZF, "Z"),
                      self.state(cpu.F, HF, "H"),
                      self.state(cpu.F, PVF, "P/V"),
                      self.state(cpu.F, NF, "N"),
                      self.state(cpu.F, CF, "C")))

    def print_stack(self, cpu, count=8):
        sp = cpu.SP
        for i in range(count):
            addr = (sp + i * 2) & 0xFFFF
            lo = cpu.ram[addr]
            hi = cpu.ram[(addr + 1) & 0xFFFF]
            value = (hi << 8) | lo
            marker = " <-- SP" if i == 0 else ""
            print("  {:04X}: {:04X}{}".format(addr, value, marker))

    def print_status(self, cpu):
        self.print16bitregs(cpu)
        self.printflags(cpu)
        self.disasm_at(cpu, cpu.pc, 1)

    def stop(self, cpu):
        self.print_status(cpu)
        while True:
            cmd = input("> ")
            if cmd == "":
                cmd = self.lastInput

            self.lastInput = cmd
            if "ir" == cmd:
                self.print8bitregs(cpu)
                self.print8bitregsprim(cpu)
            elif "if" == cmd:
                self.printflags(cpu)
            elif "ir16" == cmd:
                self.print16bitregs(cpu)
                self.print16bitregsprim(cpu)
            elif cmd == "d" or cmd.startswith("d "):
                if " " in cmd:
                    addr = self.getAddr(cmd)
                else:
                    addr = cpu.pc
                self.disasm_at(cpu, addr)
            elif cmd.startswith("m "):
                addr = self.getAddr(cmd)
                self.hexdump(cpu, addr)
            elif "pram " in cmd:
                addr = self.getAddr(cmd)
                print("RAM value at: 0x{:04X} is 0x{:02X}"
                      .format(addr, cpu.ram[addr]))
            elif "bl" == cmd:
                print("List of breakpoints:")
                self.printBreakpoints()
            elif "bc " in cmd:
                addr = self.getAddr(cmd)
                self.clearBreakpoint(addr)
                print("Breakpoint cleared at: {:04X}".format(addr))
            elif "bd " in cmd:
                addr = self.getAddr(cmd)
                self.disableBreakpoint(addr)
                print("Breakpoint disabled at: {:04X}".format(addr))
            elif "b " in cmd:
                addr = self.getAddr(cmd)
                self.setBreakpoint(addr)
                print("Breakpoint set at: {:04X}".format(addr))
            elif "s" == cmd:
                self.isSingleStepping = True
                break
            elif "c" == cmd:
                break
            elif "t" == cmd:
                print("m-cycles: {}, t-states: {}".format(cpu.m_cycles,
                                                          cpu.t_states))
            elif cmd == "stack" or cmd.startswith("stack "):
                parts = cmd.split()
                count = int(parts[1]) if len(parts) > 1 else 8
                self.print_stack(cpu, count)
            elif cmd == "trace on":
                self.trace_enabled = True
                print("Trace recording enabled ({} entries max)".format(self.trace_size))
            elif cmd == "trace off":
                self.trace_enabled = False
                print("Trace recording disabled")
            elif cmd == "trace" or cmd.startswith("trace "):
                parts = cmd.split()
                count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
                self.print_trace(cpu, count)
            elif "log" == cmd:
                self.attachDetachLogger(cpu)
            elif "?" == cmd:
                print(self.help())
            elif "exit" == cmd or "q" == cmd:
                sys.exit()
            else:
                print("unknown command")
                print(self.help())

    def isBreakpoint(self, pc):
        return pc in self.breakpoints and self.breakpoints[pc]

    def isHook(self, pc):
        return (pc in self.hooks and self.hooks[pc] is not None) or \
               (-1 in self.hooks and self.hooks[-1] is not None)

    def getHookAddr(self, pc):
        return -1 if pc not in self.hooks else pc

    def record_trace(self, pc, cpu):
        if self.trace_enabled:
            self.trace_buffer.append((pc, cpu.AF, cpu.BC, cpu.DE, cpu.HL, cpu.SP))
            if len(self.trace_buffer) > self.trace_size:
                self.trace_buffer.pop(0)

    def print_trace(self, cpu, count=20):
        entries = self.trace_buffer[-count:]
        if not entries:
            print("Trace buffer empty. Use 'trace on' to enable.")
            return
        for pc, af, bc, de, hl, sp in entries:
            op = cpu.ram[pc]
            if op in self._OPCODES:
                mnemonic = self._OPCODES[op]
            elif 0x40 <= op <= 0x7F and op != 0x76:
                mnemonic = 'LD {},{}'.format(self._REG8[(op>>3)&7], self._REG8[op&7])
            elif 0x80 <= op <= 0xBF:
                mnemonic = '{}{}'.format(self._ALU[(op>>3)&7], self._REG8[op&7])
            else:
                mnemonic = '{:02X}'.format(op)
            print('{:04X}  {:<16s} AF={:04X} BC={:04X} DE={:04X} HL={:04X} SP={:04X}'.format(
                pc, mnemonic, af, bc, de, hl, sp))

    def next_opcode(self, pc, cpu):
        if self.isHook(pc):
            return self.hooks[self.getHookAddr(pc)](cpu)
        self.record_trace(pc, cpu)
        if (self.isBreakpoint(pc)) or self.isSingleStepping:
            if self.isSingleStepping is False:
                print("Stopped...@ 0x{:04X}".format(pc))
            self.isSingleStepping = False
            self.stop(cpu)
        return False