#Timex 2048
import io
from cpu import CPU
from loggers import Logger
from debugger import Debugger

if __name__ == '__main__':
	print("Starting execution...");
	debugger = Debugger()
	debugger.setBrekpoint(0x11CB)
	debugger.setBrekpoint(0x11E2)
	timex = CPU(debugger=debugger);
	timex.run();
	print("Ending...")