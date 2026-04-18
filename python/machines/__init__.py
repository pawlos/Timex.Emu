# Machine registry.
# Each factory takes (params: dict, debugger: Debugger) and returns
# (cpu: CPU, machine_or_none). machine is None when --no-display is set,
# in which case emulate.py runs the cpu directly without the Machine loop.

from machines.timex2048 import factory as _timex2048_factory

MACHINES = {
    "timex2048": _timex2048_factory,
}
