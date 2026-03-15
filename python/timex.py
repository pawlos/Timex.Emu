#Timex 2048
from cpu import CPU
from rom import ROM
from ram import RAM
from loggers import Logger
from debugger import Debugger
from display import Display
from opcodes import *
from tape import TapeFile
import sys
import getopt


LD_BYTES = 0x0556


def make_tape_load_hook(tape):
    def tape_load_hook(cpu):
        # At 0x0556 entry: A = flag byte, F carry = LOAD(1)/VERIFY(0)
        # (EX AF,AF' hasn't executed yet when hook fires)
        # DE = expected length, IX = destination address
        expected_flag = cpu.A
        is_load = cpu.CFlag

        block = tape.next_block()
        if block is None:
            print("[!] Tape: no more blocks")
            cpu.CFlag = False  # signal failure
            Opcodes.ret(cpu, 0xC9, cpu.logger)
            return True

        if block.flag != expected_flag:
            print("[!] Tape: flag mismatch (expected 0x{:02X}, got 0x{:02X})".format(
                expected_flag, block.flag))
            cpu.CFlag = False
            Opcodes.ret(cpu, 0xC9, cpu.logger)
            return True

        if is_load:
            # Copy data to RAM at IX, up to DE bytes
            length = min(len(block.data), cpu.DE)
            for i in range(length):
                cpu.ram[cpu.IX + i] = block.data[i]
            print("[+] Tape: loaded {} bytes at 0x{:04X} (flag=0x{:02X})".format(
                length, cpu.IX, block.flag))
        else:
            print("[+] Tape: verified block (flag=0x{:02X})".format(block.flag))

        cpu.CFlag = True  # signal success
        Opcodes.ret(cpu, 0xC9, cpu.logger)
        return True

    return tape_load_hook

def systemError(cpu):
    print('System error')
    Opcodes.hlt(cpu, 0x76, cpu.logger)
    return True

def systemPrintChar(cpu):
    print(chr(cpu.A), end='')
    Opcodes.ret(cpu, 0xC9, cpu.logger)
    return True

def usage():
    print(f'Supperted parameters:')
    print(f'attach-logger - attaching logger')
    print(f'hook-system - provides python replacement for Timex 2048 system functions')
    print(f'rom=<name> - file that contains the system rom')
    print(f'mapAt=0x1234 - information at what address the program shall be mapped')
    print(f'startAt=0x1234 - instruction pointer starting address')
    print(f'program=<name> - file that contains user program')
    print(f'breakAt=0x1234 - allwos setting the breakpoint before program starts')
    print(f'help - this info')


if __name__ == '__main__':
    argv = sys.argv[1:]
    options, args = getopt.getopt(argv, "",
                               ["attach-logger",
                                "hook-system",
                                "rom=",
                                "mapAt=",
                                "startAt=",
                                "program=",
                                "breakAt=",
                                "no-display",
                                "scale=",
                                "tape=",
                                "help"])
    debugger = Debugger()

    params = {
        'debugger': False,
        'rom_file': None,
        'mapAt': 0x0,
        'break_at': None,
        'program': None,
        'startAt': 0x0,
        'hookSystem': False,
        'noDisplay': False,
        'scale': 2,
        'tape': None}
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
        if name == '--scale':
            params['scale'] = int(value)
            print(f'[+] Display scale: {value}x.')
        if name == '--tape':
            params['tape'] = value
            print(f'[+] Tape file: {value}')
        if name == '--no-display':
            params['noDisplay'] = True
            print(f'[+] Display disabled.')
        if name == "--help":
            usage()
            sys.exit()

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
        debugger.setHook(0x08, systemError)
        debugger.setHook(0x10, systemPrintChar)

    if params['tape'] is not None:
        tape = TapeFile(params['tape'])
        debugger.setHook(LD_BYTES, make_tape_load_hook(tape))

    display = None if params['noDisplay'] else Display(scale=params['scale'])

    timex = CPU(debugger=debugger, rom=rom, ram=ram, display=display)

    if params['debugger']:
        timex.logger = Logger(timex)

    print("Starting execution...")
    try:
        timex.run(params['startAt'])
    except (SystemExit, KeyboardInterrupt):
        pass
    finally:
        if display:
            display.close()
    print("Ending...")
