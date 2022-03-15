#Z80 debugger
import sys
import re
from regs import ZF, SF, HF, PVF, NF, CF, A, B, C, D, E, H, L
from utility import Bits
from loggers import EmptyLogger, Logger


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

    def help(self):
        print("available commands")
        print("ir - print info about 8-bit registers")
        print("if - print info about flags")
        print("ir16 - print info about 16-bit registers")
        print("prom 0x<addr> - print value from ROM at <addr>")
        print("pram 0x<addr> - print value from RAM at <addr>")
        print("b 0x<addr> - set a breakpoint at <addr>")
        print("bc 0x<addr> - clear a breakpoint at <addr>")
        print("bd 0x<addr> - disable a breakpoint at <addr>")
        print("bl - list all breakpoints")
        print("log - attach/detach logger")
        print("s - single step")
        print("c - continue")
        print("t - print timing info (m-cycles, t-states)")
        print("? - this help")
        print("exit - stop the program")

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
<<<<<<< HEAD
              .format(cpu.BC, cpu.DE, cpu.HL, cpu.IX, cpu.IY, cpu.SP))
=======
              .format(cpu.AF, cpu.BC, cpu.DE, cpu.HL, cpu.IX, cpu.IY, cpu.SP))

    def print16bitregsprim(self, cpu):
        print("AF': {:04X} "
              "BC': {:04X} "
              "DE': {:04X} "
              "HL': {:04X}"
              .format(cpu.AFPrim, cpu.BCPrim, cpu.DEPrim, cpu.HLPrim))

>>>>>>> task/debugger

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

    def stop(self, cpu):
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
            elif "log" == cmd:
                self.attachDetachLogger(cpu)
            elif "?" == cmd:
                print(self.help())
            elif "exit" == cmd:
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

    def next_opcode(self, pc, cpu):
        if self.isHook(pc):
            return self.hooks[self.getHookAddr(pc)](cpu)
        if (self.isBreakpoint(pc)) or self.isSingleStepping:
            if self.isSingleStepping is False:
                print("Stopped...@ 0x{:04X}".format(pc))
            self.isSingleStepping = False
            self.stop(cpu)
        return False