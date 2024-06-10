#Timex 2048
from cpu import CPU
from rom import ROM
from loggers import Logger
from debugger import Debugger
import sys
import getopt

if __name__ == '__main__':
    argv = sys.argv[1:]
    options, args = getopt.getopt(argv, "",
                               ["attach-logger",
                                "rom=",
                                "mapAt="])
    debugger = Debugger()
    debugger.setBreakpoint(0x100)

    attach_logger = False
    rom_loaded = False
    mapAt = 0x0
    rom = ROM()
    for name, value in options:
        if name == '--mapAt':
            mapAt = int(value, 16)
            rom = ROM(mapAt=mapAt)
            print(f'[+] Mapping ROM at 0x{mapAt:04X}.')
        if name == '--rom':
            rom.loadFrom(value, False)
            print(f'[+] ROM loaded from {value}.')
            rom_loaded = True
        if name =='--attach-logger':
            attach_logger = True
            print(f'[+] Logger attached.')

    if not rom_loaded:
        rom.loadFrom('../rom/tc2048.rom')

    timex = CPU(debugger=debugger, rom=rom)

    if attach_logger:
        timex.logger = Logger(timex)

    print("Starting execution...")
    timex.run(mapAt)
    print("Ending...")
