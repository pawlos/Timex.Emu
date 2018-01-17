#Z80 debugger
import sys
import re
from regs import *
from utility import Bits
from loggers import *

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
		self.lastInput = ""

	def setBreakpoint(self, pc):
		self.breakpoints[pc] = True

	def disableBreakpoint(self, pc):
		if pc in self.breakpoints:
			self.breakpoints[pc] = False

	def clearBreakpoint(self, pc):
		if pc in self.breakpoints:
			del self.breakpoints[pc]

	def getAddr(self, input):
		return int(re.search('0x([0-9a-fA-F]+)$', input).group(1), base=16)

	def printBreakpoints(self):
		for pc in self.breakpoints:
			print "Breakpoint at {:04X}, {}".format(pc, "active" if self.breakpoints[pc] else "inactive")

	def attachDetachLogger(self, cpu):
		if type(cpu.logger) is not EmptyLogger:
			print "Detaching logger"
			cpu.logger = EmptyLogger()
		else:
			print "Attaching logger"
			cpu.logger = Logger(cpu)

	def help(self):
		print "available commands"
		print "ir - print info about 8-bit registers"
		print "if - print info about flags"
		print "ir16 - print info about 16-bit registers"
		print "prom 0x<addr> - print value from ROM at <addr>"
		print "pram 0x<addr> - print value from RAM at <addr>"
		print "b 0x<addr> - set a breakpoint at <addr>"
		print "bc 0x<addr> - clear a breakpoint at <addr>"
		print "bd 0x<addr> - disable a breakpoint at <addr>"
		print "bl - list all breakpoints"
		print "log - attach/detach logger"
		print "s - single step"
		print "c - continue"
		print "? - this help"

	def state(self, flag, flag_bit, flag_name):
		return flag_name if Bits.getNthBit(flag,flag_bit) == True else flag_name.lower()

	def stop(self, cpu):
		while True:
			input = raw_input("> ")
			if input == "":
				input = self.lastInput

			self.lastInput = input
			if "ir" == input:
				print "A : {:02X} B : {:02X} C : {:02X} D : {:02X} E : {:02X} H : {:02X} L : {:02X}" \
					.format(cpu.regs[A], cpu.regs[B], cpu.regs[C],  cpu.regs[D],  cpu.regs[E], cpu.regs[H], cpu.regs[L])
				print "A': {:02X} B': {:02X} C': {:02X} D': {:02X} E': {:02X} H': {:02X} L': {:02X}" \
					.format(cpu.regsPri[A], cpu.regsPri[B], cpu.regsPri[C], cpu.regsPri[D], cpu.regsPri[E], cpu.regsPri[H], cpu.regsPri[L])
			elif "if" == input:
				print "{} {} _ {} _ {} {} {}".format(self.state(cpu.F, SF, "S"), self.state(cpu.F, ZF, "Z"), \
													 self.state(cpu.F, HF, "H"), self.state(cpu.F, PVF, "P/V"), \
													 self.state(cpu.F, NF, "N"), self.state(cpu.F, CF, "C"))
			elif "ir16" == input:
				print "BC : {:04X} DE : {:04X} HL : {:04X} IX : {:04X} IY : {:04X} SP : {:04X}".format(cpu.BC, cpu.DE, cpu.HL, cpu.IX, cpu.IY, cpu.SP)
			elif "prom " in input:
				addr = self.getAddr(input)
				print "Rom value at: 0x{:04X} is 0x{:02X}".format(addr, cpu.rom.readMemory(addr))
			elif "pram " in input:
				addr = self.getAddr(input)
				print "Ram value at: 0x{:04X} is 0x{:02X}".format(addr, cpu.ram.readAddr(addr))
			elif "bl" == input:
				print "List of breakpoints:"
				self.printBreakpoints()
			elif "bc " in input:
				addr = self.getAddr(input)
				self.clearBreakpoint(addr)
				print "Breakpoint cleared at: {:04X}".format(addr)
			elif "bd " in input:
				addr = self.getAddr(input)
				self.disableBreakpoint(addr)
				print "Breakpoint disabled at: {:04X}".format(addr)
			elif "b " in input:
				addr = self.getAddr(input)
				self.setBreakpoint(addr)
				print "Breakpoint set at: {:04X}".format(addr)
			elif "s" == input:
				self.isSingleStepping = True
				break
			elif "c" == input:
				break
			elif "log" == input:
				self.attachDetachLogger(cpu)
			elif "?" == input:
				print self.help()
			else:
				print "unknown command"
				print self.help()

	def next_opcode(self, pc, cpu):
		if (pc in self.breakpoints and self.breakpoints[pc]) or self.isSingleStepping:
			if self.isSingleStepping == False:
				print "Stopped...@ 0x{:04X}".format(pc)
			self.isSingleStepping = False
			self.stop(cpu)