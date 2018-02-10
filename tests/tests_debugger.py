
import unittest
from debugger import *

class tests_debugger(unittest.TestCase):
	
	def test_init_zeros_registers(self):
		debugger = Debugger()
		self.assertFalse(debugger.isSingleStepping)

	def test_setBrakpoint_adds_a_breakpoint(self):
		debugger = Debugger()
		debugger.setBreakpoint(0x1111)
		self.assertTrue(debugger.breakpoints[0x1111])

	def test_disableBreakpoint_sets_breakpoint_to_false(self):
		debugger = Debugger()
		debugger.setBreakpoint(0x2222)

		debugger.disableBreakpoint(0x2222)
		self.assertFalse(debugger.breakpoints[0x2222])

	def test_clearBreakpoint_sets_breakpoint_to_false(self):
		debugger = Debugger()
		debugger.setBreakpoint(0x2222)

		debugger.clearBreakpoint(0x2222)
		self.assertTrue(0x2222 not in debugger.breakpoints)

