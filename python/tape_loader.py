# Tape loading hook for ROM trap at LD-BYTES (0x0556)

from opcodes import Opcodes
from screen import COLORS

BYTES_PER_FRAME = 256
STRIPE_PAIRS = [
    (COLORS[2], COLORS[5]),  # red / cyan
    (COLORS[1], COLORS[6]),  # blue / yellow
]


class TapeLoader:
    def __init__(self, tape):
        self._tape = tape
        self.machine = None

    def rewind(self):
        self._tape.rewind()

    def hook(self, cpu):
        expected_flag = cpu.A
        is_load = cpu.CFlag

        block = self._tape.next_block()
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
            machine = self.machine
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
