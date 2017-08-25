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

	def state(self, flag, flag_name):
		return flag_name if flag == True else flag_name.lower()

	def stop(self, regs, regsPri, flags):
		while True:
			input = raw_input()
			if "ir" == input:
				print "A : {:02X} B : {:02X} C : {:02X} D : {:02X} E : {:02X} H : {:02X} L : {:02X}" \
					.format(regs[A], regs[B], regs[C],  regs[D],  regs[E], regs[H], regs[L])
				print "A': {:02X} B': {:02X} C': {:02X} D': {:02X} E': {:02X} H': {:02X} L': {:02X}" \
					.format(regsPri[A], regsPri[B], regsPri[C], regsPri[D], regsPri[E], regsPri[H], regsPri[L])
			elif "if" == input:
				print "{} {} _ {} _ {} {} {}".format(self.state(flags[SF], "S"), self.state(flags[ZF], "Z"), \
													 self.state(flags[HF], "H"), self.state(flags[PVF], "P/V"), \
													 self.state(flags[NF], "N"), self.state(flags[CF], "C"))
			elif "" == input:
				break
			else:
				print "unknown command"

	def next_opcode(self, pc, regs, regsPri, flags):
		if pc in self.breakpoints and self.breakpoints[pc]:
			print "Stopped...@ 0x{:4X}".format(pc)
			self.stop(regs, regsPri, flags)