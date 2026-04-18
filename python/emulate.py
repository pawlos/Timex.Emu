# Single CLI entry — dispatches to a machine factory by --machine name.

import sys
import getopt

from debugger import Debugger
from snapshot import load_z80
from machines import MACHINES


def usage():
    print('Supported parameters:')
    print('  --machine=<name>       machine to emulate (default: timex2048).')
    print('                         Known:', ', '.join(sorted(MACHINES)))
    print('  --attach-logger        attach instruction logger')
    print('  --hook-system          replace Timex 2048 system calls with python stubs')
    print('  --rom=<file>           system ROM file')
    print('  --mapAt=0x1234         map ROM at this address')
    print('  --startAt=0x1234       initial PC')
    print('  --program=<file>       user program to load at 0x8000')
    print('  --breakAt=0x1234       set an initial breakpoint')
    print('  --scale=N              display scale (default 2)')
    print('  --tape=<file>          .tap file to load')
    print('  --tape-mode=trap|pulse tape emulation strategy (default trap)')
    print('  --z80=<file>           .z80 snapshot to load')
    print('  --no-display           run headless (no pygame window)')
    print('  --debug                periodic PC/register logging')
    print('  --help                 this text')


def parse_args(argv):
    options, _ = getopt.getopt(argv, "",
                               ["machine=",
                                "attach-logger",
                                "hook-system",
                                "rom=",
                                "mapAt=",
                                "startAt=",
                                "program=",
                                "breakAt=",
                                "no-display",
                                "scale=",
                                "tape=",
                                "tape-mode=",
                                "z80=",
                                "debug",
                                "help"])

    params = {
        'machine': 'timex2048',
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
        'tape_mode': 'trap',
        'z80': None,
        'debug': False,
    }

    for name, value in options:
        if name == '--machine':
            params['machine'] = value
            print(f'[+] Machine: {value}')
        elif name == '--mapAt':
            params['mapAt'] = int(value, 16)
            print(f"[+] Mapping ROM at 0x{params['mapAt']:04X}.")
        elif name == '--startAt':
            params['startAt'] = int(value, 16)
            print(f"[+] Starting at: 0x{params['startAt']:04X}.")
        elif name == '--rom':
            params['rom_file'] = value
            print(f'[+] ROM loaded from {value}.')
        elif name == '--attach-logger':
            params['debugger'] = True
            print('[+] Debugger attached.')
        elif name == '--breakAt':
            params['break_at'] = int(value, 16)
            print(f"[+] Setting breakpoint at 0x{params['break_at']:04X}.")
        elif name == '--program':
            params['program'] = value
            print(f'[+] Loading program: {value}')
        elif name == '--hook-system':
            params['hookSystem'] = True
            print('[+] Hooking system functions')
        elif name == '--scale':
            params['scale'] = int(value)
            print(f'[+] Display scale: {value}x.')
        elif name == '--tape':
            params['tape'] = value
            print(f'[+] Tape file: {value}')
        elif name == '--tape-mode':
            if value not in ('trap', 'pulse'):
                print(f"[!] --tape-mode must be 'trap' or 'pulse', got {value!r}")
                sys.exit(1)
            params['tape_mode'] = value
            print(f'[+] Tape mode: {value}')
        elif name == '--z80':
            params['z80'] = value
            print(f'[+] Z80 snapshot: {value}')
        elif name == '--no-display':
            params['noDisplay'] = True
            print('[+] Display disabled.')
        elif name == '--debug':
            params['debug'] = True
            print('[+] Debug output enabled.')
        elif name == '--help':
            usage()
            sys.exit()
    return params


def main(argv=None):
    params = parse_args(sys.argv[1:] if argv is None else argv)

    if params['machine'] not in MACHINES:
        print(f"[!] Unknown --machine={params['machine']!r}. "
              f"Known: {', '.join(sorted(MACHINES))}")
        sys.exit(1)

    debugger = Debugger()
    if params['break_at'] is not None:
        debugger.setBreakpoint(params['break_at'])

    try:
        cpu, machine = MACHINES[params['machine']](params, debugger)
    except FileNotFoundError as e:
        print(f"[!] File not found: {e.filename}")
        sys.exit(1)

    start_pc = params['startAt']
    border = None
    if params['z80'] is not None:
        try:
            border = load_z80(params['z80'], cpu)
            start_pc = cpu.pc
        except FileNotFoundError:
            print(f"[!] File not found: {params['z80']}")
            sys.exit(1)

    if machine is None:
        print("Starting execution...")
        try:
            cpu.run(start_pc)
        except (SystemExit, KeyboardInterrupt):
            pass
    else:
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


if __name__ == '__main__':
    main()
