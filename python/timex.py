#!/usr/bin/env python3
# Backwards-compatible entry for the Timex 2048 machine.
# Forwards to emulate.py with --machine=timex2048 if not overridden.

import sys
from emulate import main

if __name__ == '__main__':
    if not any(a.startswith('--machine') for a in sys.argv[1:]):
        sys.argv.insert(1, '--machine=timex2048')
    main()
