#Z80 debugger
import sys
import re
from regs import ZF, SF, HF, PVF, NF, CF, A, B, C, D, E, H, L
from utility import Bits
from loggers import EmptyLogger, Logger
from disassembler import Disassembler

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
        match = re.search('0x([0-9a-fA-F]+)$', input)
        if not match:
            print("Invalid address. Use 0x followed by hex digits (e.g. 0x4000)")
            return None
        return int(match.group(1), base=16)

    def printBreakpoints(self):
        for pc in self.breakpoints:
            state = "active" if self.breakpoints[pc] else "inactive"
            print("Breakpoint at {:04X}, {}"
                  .format(pc, state))

    def attachDetachLogger(self, cpu):
        if not isinstance(cpu.logger, EmptyLogger):
            print("Detaching logger")
            cpu.logger = EmptyLogger()
        else:
            print("Attaching logger")
            cpu.logger = Logger(cpu)

    _disasm = Disassembler()

    def disasm_at(self, cpu, addr, count=8):
        self._disasm.disasm(cpu.ram, addr, count)

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
        print("n - step over (skip into CALL/RST)")
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
            try:
                cmd = input("> ")
            except EOFError:
                break
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
                    if addr is None: continue
                else:
                    addr = cpu.pc
                self.disasm_at(cpu, addr)
            elif cmd.startswith("m "):
                addr = self.getAddr(cmd)
                if addr is not None:
                    self.hexdump(cpu, addr)
            elif "pram " in cmd:
                addr = self.getAddr(cmd)
                if addr is not None:
                    print("RAM value at: 0x{:04X} is 0x{:02X}"
                          .format(addr, cpu.ram[addr]))
            elif "bl" == cmd:
                print("List of breakpoints:")
                self.printBreakpoints()
            elif "bc " in cmd:
                addr = self.getAddr(cmd)
                if addr is not None:
                    self.clearBreakpoint(addr)
                    print("Breakpoint cleared at: {:04X}".format(addr))
            elif "bd " in cmd:
                addr = self.getAddr(cmd)
                if addr is not None:
                    self.disableBreakpoint(addr)
                    print("Breakpoint disabled at: {:04X}".format(addr))
            elif "b " in cmd:
                addr = self.getAddr(cmd)
                if addr is not None:
                    self.setBreakpoint(addr)
                    print("Breakpoint set at: {:04X}".format(addr))
            elif "s" == cmd:
                self.isSingleStepping = True
                break
            elif "n" == cmd:
                # Step over: if current instruction is CALL/RST, run until return
                op = cpu.ram[cpu.pc]
                is_call = op == 0xCD or (op & 0xC7) == 0xC4  # CALL nn / CALL cc,nn
                is_rst = (op & 0xC7) == 0xC7                  # RST xx
                if is_call:
                    next_pc = (cpu.pc + 3) & 0xFFFF
                    self._step_over_bp = next_pc
                    self.setBreakpoint(next_pc)
                    break
                elif is_rst:
                    next_pc = (cpu.pc + 1) & 0xFFFF
                    self._step_over_bp = next_pc
                    self.setBreakpoint(next_pc)
                    break
                else:
                    # Not a call — behave like single step
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
                self.help()
            elif "exit" == cmd or "q" == cmd:
                sys.exit()
            else:
                print("unknown command")
                self.help()

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
            mnemonic, _ = self._disasm.decode(cpu.ram, pc)
            print('{:04X}  {:<16s} AF={:04X} BC={:04X} DE={:04X} HL={:04X} SP={:04X}'.format(
                pc, mnemonic, af, bc, de, hl, sp))

    def next_opcode(self, pc, cpu):
        if self.isHook(pc):
            return self.hooks[self.getHookAddr(pc)](cpu)
        self.record_trace(pc, cpu)
        # Clean up step-over breakpoint
        step_over = getattr(self, '_step_over_bp', None)
        if step_over is not None and pc == step_over:
            self.clearBreakpoint(step_over)
            self._step_over_bp = None
        if (self.isBreakpoint(pc)) or self.isSingleStepping:
            if self.isSingleStepping is False:
                print("Stopped...@ 0x{:04X}".format(pc))
            self.isSingleStepping = False
            self.stop(cpu)
        return False