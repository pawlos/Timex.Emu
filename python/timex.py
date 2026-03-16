#Timex 2048
from cpu import CPU
from rom import ROM
from ram import RAM
from loggers import Logger
from debugger import Debugger
from machine import Machine
from opcodes import *
from tape import TapeFile
from snapshot import load_z80
import sys
import getopt


LD_BYTES = 0x0556


def make_tape_load_hook(tape, machine_ref):
    # machine_ref is a list so we can set it after Machine is created
    from screen import COLORS
    BYTES_PER_FRAME = 256
    # Stripe color pairs: (color1, color2)
    STRIPE_PAIRS = [
        (COLORS[2], COLORS[5]),  # red / cyan
        (COLORS[1], COLORS[6]),  # blue / yellow
    ]

    def tape_load_hook(cpu):
        expected_flag = cpu.A
        is_load = cpu.CFlag

        block = tape.next_block()
        if block is None:
            print("[!] Tape: no more blocks")
            cpu.CFlag = False
            Opcodes.ret(cpu, 0xC9, cpu.logger)
            return True

        if block.flag != expected_flag:
            print("[!] Tape: flag mismatch (expected 0x{:02X}, got 0x{:02X})".format(
                expected_flag, block.flag))
            cpu.CFlag = False
            Opcodes.ret(cpu, 0xC9, cpu.logger)
            return True

        if is_load:
            length = min(len(block.data), cpu.DE)
            machine = machine_ref[0] if machine_ref else None
            for i in range(length):
                cpu.ram[cpu.IX + i] = block.data[i]
                if machine and i % BYTES_PER_FRAME == 0:
                    pair_idx = (block.data[i] >> 4) & 1
                    machine.screen.loading_stripes = STRIPE_PAIRS[pair_idx]
                    machine.screen.render(cpu.ram)
                    machine.keyboard.handle_events(machine.screen, machine.joystick, machine)
                    machine._clock.tick(50)
            if machine:
                machine.screen.loading_stripes = None
                machine.screen.set_border(7)
            print("[+] Tape: loaded {} bytes at 0x{:04X} (flag=0x{:02X})".format(
                length, cpu.IX, block.flag))
        else:
            print("[+] Tape: verified block (flag=0x{:02X})".format(block.flag))

        cpu.CFlag = True
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
                                "z80=",
                                "debug",
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
        'tape': None,
        'z80': None,
        'debug': False}
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
        if name == '--z80':
            params['z80'] = value
            print(f'[+] Z80 snapshot: {value}')
        if name == '--no-display':
            params['noDisplay'] = True
            print(f'[+] Display disabled.')
        if name == '--debug':
            params['debug'] = True
            print(f'[+] Debug output enabled.')
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

    machine_ref = [None]  # mutable ref, set after Machine is created

    if params['tape'] is not None:
        try:
            tape = TapeFile(params['tape'])
        except FileNotFoundError:
            print("[!] File not found: {}".format(params['tape']))
            sys.exit(1)
        debugger.setHook(LD_BYTES, make_tape_load_hook(tape, machine_ref))

    cpu = CPU(debugger=debugger, rom=rom, ram=ram)

    if params['debugger']:
        cpu.logger = Logger(cpu)

    start_pc = params['startAt']
    border = None

    if params['z80'] is not None:
        try:
            border = load_z80(params['z80'], cpu)
            start_pc = cpu.pc  # snapshot sets PC
        except FileNotFoundError:
            print("[!] File not found: {}".format(params['z80']))
            sys.exit(1)

    if params['noDisplay']:
        print("Starting execution...")
        try:
            cpu.run(start_pc)
        except (SystemExit, KeyboardInterrupt):
            pass
    else:
        machine = Machine(cpu, scale=params['scale'], debug=params['debug'])
        machine_ref[0] = machine
        if border is not None:
            machine.screen.set_border(border)
        print("Starting execution...")
        try:
            machine.run(start_pc)
        except (SystemExit, KeyboardInterrupt):
            pass
        finally:
            machine.close()
    print("Ending...")
