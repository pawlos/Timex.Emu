#Z80 debugger
import sys
from regs import *

class EmptyDebugger(object):
	def setBreakpoint(self, pc):
		pass

	def stop(self):
		pass

	def next_opcode(self, pc):
		pass


class Debugger(object):
	def __init__(self):
		self.isSingleStepping = False
		self.breakpoints = {}

	def setBrekpoint(self, pc):
		self.breakpoints[pc] = True

	def stop(self, regs, regsPri):
		while True:
			input = raw_input()
			if "ir" == input:
				print "A : {:02X} B : {:02X} C : {:02X} D : {:02X} E : {:02X} H : {:02X} L : {:02X}" \
					.format(regs[A], regs[B], regs[C],  regs[D],  regs[E], regs[H], regs[L])
				print "A': {:02X} B': {:02X} C': {:02X} D': {:02X} E': {:02X} H': {:02X} L': {:02X}" \
					.format(regsPri[A], regsPri[B], regsPri[C], regsPri[D], regsPri[E], regsPri[H], regsPri[L])
			if "" == input:
				break

			print "unknown command"

	def next_opcode(self, pc, regs, regsPri):
		if pc in self.breakpoints and self.breakpoints[pc]:
			print "Stopped...@ 0x{:4X}".format(pc)
			self.stop(regs, regsPri)