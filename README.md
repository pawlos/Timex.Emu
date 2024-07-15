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
