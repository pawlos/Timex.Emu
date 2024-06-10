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
    rom_file = None
    mapAt = 0x0
    rom = ROM()
    for name, value in options:
        if name == '--mapAt':
            mapAt = int(value, 16)
            print(f'[+] Mapping ROM at 0x{mapAt:04X}.')
        if name == '--rom':
            rom_file = value
            print(f'[+] ROM loaded from {value}.')
        if name =='--attach-logger':
            attach_logger = True
            print(f'[+] Logger attached.')

    if mapAt != 0x0:
        rom = ROM(mapAt = mapAt)
    if rom_file is None:
        rom.loadFrom('../rom/tc2048.rom')
    else:
        rom.loadFrom(rom_file, False)

    timex = CPU(debugger=debugger, rom=rom)

    if attach_logger:
        timex.logger = Logger(timex)

    print("Starting execution...")
    timex.run(mapAt)
    print("Ending...")
