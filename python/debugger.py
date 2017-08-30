#Z80 debugger
import sys
import re
from regs import *

class EmptyDebugger(object):
	def setBreakpoint(self, pc):
		pass

	def stop(self):
		pass

	def next_opcode(self, pc, cpu):
		pass


class Debugger(object):
	def __init__(self):
		self.isSingleStepping = False
		self.breakpoints = {}

	def setBrekpoint(self, pc):
		self.breakpoints[pc] = True

	def state(self, flag, flag_name):
		return flag_name if flag == True else flag_name.lower()

	def stop(self, cpu):
		while True:
			input = raw_input()
			if "ir" == input:
				print "A : {:02X} B : {:02X} C : {:02X} D : {:02X} E : {:02X} H : {:02X} L : {:02X}" \
					.format(cpu.regs[A], cpu.regs[B], cpu.regs[C],  cpu.regs[D],  cpu.regs[E], cpu.regs[H], cpu.regs[L])
				print "A': {:02X} B': {:02X} C': {:02X} D': {:02X} E': {:02X} H': {:02X} L': {:02X}" \
					.format(cpu.regsPri[A], cpu.regsPri[B], cpu.regsPri[C], cpu.regsPri[D], cpu.regsPri[E], cpu.regsPri[H], cpu.regsPri[L])
			elif "if" == input:
				print "{} {} _ {} _ {} {} {}".format(self.state(cpu.flags[SF], "S"), self.state(cpu.flags[ZF], "Z"), \
													 self.state(cpu.flags[HF], "H"), self.state(cpu.flags[PVF], "P/V"), \
													 self.state(cpu.flags[NF], "N"), self.state(cpu.flags[CF], "C"))
			elif "ir16" == input:
				print "BC : {:04X} DE : {:04X} HL : {:04X} IX : {:04X} IY : {:04X}".format(cpu.BC, cpu.DE, cpu.HL, cpu.IX, cpu.IY)
			elif "prom " in input:
				addr = int(re.search('0x([0-9a-fA-F]+)$', input).group(1), base=16)
				print "Rom value at: 0x{:04X} is 0x{:02X}".format(addr, cpu.rom.readMemory(addr))
			elif "pram " in input:
				addr = int(re.search('^0x([0-9a-fA-F]+)$', input).group(1), base=16)
				print "Ram value at: 0x{:04X} is 0x{:02X}".format(addr, cpu.ram.readAddr(addr))
			elif "" == input:
				break
			else:
				print "unknown command"

	def next_opcode(self, pc, cpu):
		if pc in self.breakpoints and self.breakpoints[pc]:
			print "Stopped...@ 0x{:4X}".format(pc)
			self.stop(cpu)