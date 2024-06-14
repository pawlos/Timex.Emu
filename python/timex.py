#Timex 2048
from cpu import CPU
from rom import ROM
from ram import RAM
from loggers import Logger
from debugger import Debugger
from opcodes import *
import sys
import getopt

def systemFunction(cpu):
    print('System function')
    Opcodes.ret(cpu, 0xc9, cpu.logger)
    return True

if __name__ == '__main__':
    argv = sys.argv[1:]
    options, args = getopt.getopt(argv, "",
                               ["attach-logger",
                                "hook-system",
                                "rom=",
                                "mapAt=",
                                "startAt=",
                                "program=",
                                "breakAt="])
    debugger = Debugger()

    params = {
        'debugger': False,
        'rom_file': None,
        'mapAt': 0x0,
        'break_at': None,
        'program': None,
        'startAt': 0x0,
        'hookSystem': False}
    rom = ROM()
    ram = RAM()
    for name, value in options:
        if name == '--mapAt':
            mapAt = int(value, 16)
            params['mapAt'] = mapAt
            print(f'[+] Mapping ROM at 0x{mapAt:04X}.')
        if name == '--startAt':
            startAt = int(value, 16)
            params['startAt'] = startAt
            print(f'[+] Starting at: 0x{startAt:04X}.')
        if name == '--rom':
            params['rom_file'] = value
            print(f'[+] ROM loaded from {value}.')
        if name =='--attach-logger':
            params['debugger'] = True
            print(f'[+] Debugger attached.')
        if name =='--breakAt':
            break_at = int(value, 16)
            params['break_at'] = break_at
            print(f'[+] Setting breakpoint at 0x{break_at:04X}.')
        if name =='--program':
            params['program'] = value
            print(f'[+] Loading program: {value}')
        if name =='--hook-system':
            params['hookSystem'] = True
            print(f'[+] Hooking system functions')

    if params['mapAt'] != 0x0:
        rom = ROM(mapAt = params['mapAt'])
    if params['rom_file'] is None:
        rom.loadFrom('../rom/tc2048.rom')
    else:
        rom.loadFrom(params['rom_file'], False)

    if params['break_at'] is not None:
        debugger.setBreakpoint(params['break_at'])

    if params['program'] is not None:
        ram.loadProgramAt(params['program'], 0x8000)

    if params['hookSystem']:
        debugger.setHook(0x08, systemFunction)

    timex = CPU(debugger=debugger, rom=rom, ram=ram)

    if params['debugger']:
        timex.logger = Logger(timex)

    print("Starting execution...")
    timex.run(params['startAt'])
    print("Ending...")
