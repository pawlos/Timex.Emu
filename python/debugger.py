#Z80 debugger
import sys

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

	def stop(self):
		input = raw_input()

	def next_opcode(self, pc):
		if pc in self.breakpoints and self.breakpoints[pc]:
			print "Stopped...@ 0x{:4X}".format(pc)
			self.stop()