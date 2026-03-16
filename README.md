Timex.Emu
========

Timex.Emu is an emulator for a popular Timex 2048 machine.

Folder structure:

docs:
  - Z80 CPU Manual
  - Z80 CPU Peripherals
  - Complete ROM

python:
  - timex.py - main entry to the emulator

  Example command to load a user program:

  `python3 timex.py --program=helloworld.bin --startAt=8000 --breakAt=8000 --mapAt=8000 --hook-system`

  This loads user program `helloworld.bin` (`--program`) at `0x8000` (`--mapAt`), putting a break point at `0x8000` (`--breakAt`) and starting execution from `0x8000` too (`--startAt`). Additionally system function (i.e. `print`) are being hooked with python replacement.

  To run with display (requires pygame-ce):

  `python3 timex.py`

  To run without display:

  `python3 timex.py --no-display`

  Keyboard mapping (PC → Timex 2048):

  | PC Key | Timex 2048 |
  |--------|------------|
  | A-Z, 0-9 | Same |
  | Enter | ENTER |
  | Space | SPACE |
  | Left/Right Shift | CAPS SHIFT |
  | Left/Right Ctrl | SYMBOL SHIFT |

  Common combinations:
  - `Shift + 0` — DELETE (backspace)
  - `Ctrl + P` — " (double quote)
  - `Ctrl + Z` — : (colon)
  - `Ctrl + N` — , (comma)
  - `Ctrl + Symbol` — ; (semicolon)

  BASIC input modes:
  - **K mode** (cursor shows `K`) — default after ENTER. Single keypress gives keywords (e.g. `P` = PRINT, `G` = GOTO). Switches to L mode after first keyword.
  - **L mode** (cursor shows `L`) — lowercase letter input. Entered automatically after typing a keyword in K mode.
  - **C mode** (cursor shows `C`) — uppercase letters. Toggle with CAPS LOCK (`Shift + 2`).
  - **E mode** (cursor shows `E`) — extended keywords. Enter by pressing `Shift + Ctrl` together. Then press a key (with or without `Ctrl`) to get extended keywords like BEEP, INK, PAPER, etc.
  - **G mode** (cursor shows `G`) — graphics characters. Enter with `Shift + 9`.

  Emulator keys:
  - `F1` — pause / resume
  - `F2` — open interactive debugger (in terminal)
  - `F12` — save screenshot as PNG
  - `Arrow keys` — Kempston joystick directions
  - `Right Alt` — Kempston joystick fire

  Example — typing `BEEP 1,0`:
  1. Make sure you're in K mode (press ENTER if needed)
  2. `Shift + Ctrl` (enter E mode)
  3. `Ctrl + Z` (BEEP keyword)
  4. `Space`, `1`, `Ctrl + N` (comma), `0`
  5. `Enter` (execute)

  Loading games from .tap files:

  `python3 timex.py --tape=game.tap`

  Then type `LOAD ""` (press `J` then `Ctrl+P` twice) and press `Enter`.

  Additional options:
  - `--scale=3` — scale display (default 2x, use 3 or 4 for hi-res monitors)
  - `--debug` — enable periodic PC/register logging to terminal
  - `--no-display` — run headless (no pygame window)

  Debugger commands (press F2 to enter):
  | Command | Description |
  |---------|-------------|
  | `ir` | 8-bit registers |
  | `ir16` | 16-bit registers |
  | `if` | CPU flags |
  | `d [0xADDR]` | disassemble at address (default: PC) |
  | `m 0xADDR` | hex dump memory |
  | `b 0xADDR` | set breakpoint |
  | `bc 0xADDR` | clear breakpoint |
  | `bl` | list breakpoints |
  | `s` | single step |
  | `c` | continue |
  | `trace on/off` | enable/disable execution trace |
  | `trace [n]` | show last n executed instructions |
  | `stack [n]` | show stack entries (default 8) |
  | `q` | quit |

rom:
  - Binary file containing ROM of actual machine

tests:
  - a suite of unit tests
    - running tests: `python3 -m unittest discover`.

  > [!NOTE]
  > To run zexall or zexdoc tests suite set ZEXALL or ZEXDOC environment variable to True respectivly
  >
  > `export ZEXALL=True`
  >
  > `python3 -m unittest tests_cpu.tests_cpu.test_zexall`
  > `python3 -m unittest tests_cpu.tests_cpu.test_zexdoc`

Links
=====
  - [http://pl.wikipedia.org/wiki/Zilog_Z80](http://pl.wikipedia.org/wiki/Zilog_Z80)
  - [http://pl.wikipedia.org/wiki/Timex_Sinclair_2048](http://pl.wikipedia.org/wiki/Timex_Sinclair_2048)
  - [http://en.wikipedia.org/wiki/Timex_Computer_2048](http://en.wikipedia.org/wiki/Timex_Computer_2048)
  - [http://clrhome.org/table/](http://clrhome.org/table/)


[![Hits-of-Code](https://hitsofcode.com/github/pawlos/Timex.Emu)](https://hitsofcode.com/view/github/pawlos/Timex.Emu)
