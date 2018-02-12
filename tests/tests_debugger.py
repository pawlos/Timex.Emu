
import unittest
from debugger import *
from fakes import FakeCpu

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

	def test_getAddr_correctly_parses_address(self):
		debugger = Debugger()
		addr = debugger.getAddr("0x1234")
		self.assertEqual(0x1234, addr)

	def test_attachDetachLogger_attaches_logger_when_ther_is_Empty(self):
		debugger = Debugger()
		cpu = FakeCpu()
		cpu.logger = EmptyLogger()
		debugger.attachDetachLogger(cpu)

		self.assertFalse(type(cpu.logger) is EmptyLogger)

	def test_attachDetachLogger_detaches_logger_when_ther_is_not_Empty(self):
		debugger = Debugger()
		cpu = FakeCpu()
		cpu.logger = Logger(cpu)
		debugger.attachDetachLogger(cpu)

		self.assertTrue(type(cpu.logger) is EmptyLogger)
