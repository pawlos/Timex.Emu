#Timex 2048
from cpu import CPU
from loggers import Logger
from debugger import Debugger
from sys import argv

if __name__ == '__main__':
    print("Starting execution...")

    debugger = Debugger()
    debugger.setBreakpoint(0x16DD)

    timex = CPU(debugger=debugger)

    if '--attach-logger' in argv:
        timex.logger = Logger(timex)

    timex.run()
    print("Ending...")
