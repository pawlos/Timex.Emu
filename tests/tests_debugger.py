
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

