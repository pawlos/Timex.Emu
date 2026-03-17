# Timex 2048 / ZX Spectrum Machine
# Coordinates CPU, screen, keyboard, beeper, and joystick

import pygame
from screen import Screen
from keyboard import Keyboard
from beeper import Beeper
from joystick import Joystick
from snapshot import save_z80
from known_addresses import LD_BYTES

TSTATES_PER_FRAME = 69888


class Machine:
    def __init__(self, cpu, scale=2, debug=False, rom=None, tape=None, tape_hook=None):
        self.cpu = cpu
        self.rom = rom
        self.tape = tape
        self.tape_hook = tape_hook
        self.screen = Screen(scale)
        self.keyboard = Keyboard()
        self.beeper = Beeper()
        self.joystick = Joystick()
        self.debug = debug
        self.paused = False
        self.turbo = False

        # Register port handlers on CPU's I/O
        cpu.io.on_read(0xFE, self.keyboard.read)
        cpu.io.on_read(0x1F, self.joystick.read)
        cpu.io.on_write(0xFE, self._write_port_fe)

        self._frame_count = 0
        self._clock = pygame.time.Clock()

    def _write_port_fe(self, value):
        self.screen.set_border(value & 0x07)
        self.beeper.set_speaker((value >> 4) & 1, self.cpu.tstates)

    def update(self):
        self.keyboard.handle_events(self.screen, self.joystick, self)
        self.screen.render(self.cpu.ram)
        self.beeper.render_audio()

    def run(self, pc=0x0):
        cpu = self.cpu
        cpu.pc = pc
        while True:
            if self.paused:
                self.keyboard.handle_events(self.screen, self.joystick, self)
                self._clock.tick(50)
                continue
            if not cpu.halted:
                cpu.readOp()
            else:
                cpu.m_cycles, cpu.t_states = 1, 4
            cpu._checkInterrupts()
            if cpu.tstates >= TSTATES_PER_FRAME:
                cpu.tstates -= TSTATES_PER_FRAME
                cpu._interruptPending = True
                if self.turbo and self._frame_count % 10 != 0:
                    # In turbo: only render every 10th frame
                    self.keyboard.handle_events(self.screen, self.joystick, self)
                else:
                    self.update()
                    if not self.turbo:
                        self._clock.tick(50)
                self._frame_count += 1
                if self.debug and self._frame_count % 50 == 0:
                    print("PC=0x{:04X} iff1={} im={} IY=0x{:04X}".format(
                        cpu.pc, cpu.iff1, cpu.im, cpu.IY))

    def reset(self):
        # Disable tape hook during ROM init
        if self.tape_hook:
            self.cpu.debugger.setHook(LD_BYTES, None)
        self.cpu.reset()
        # Clear RAM and reload ROM
        self.cpu.ram.clear()
        if self.rom:
            self.cpu.ram.load(self.rom)
        # Rewind tape and re-enable hook
        if self.tape:
            self.tape.rewind()
        if self.tape_hook:
            self.cpu.debugger.setHook(LD_BYTES, self.tape_hook)
        print("[+] Reset")

    def save_state(self):
        import time
        filename = "state_{}.z80".format(int(time.time()))
        from screen import COLORS
        border_idx = next((i for i, c in enumerate(COLORS) if c == self.screen.border_color), 7)
        save_z80(filename, self.cpu, border_idx)

    def enter_debugger(self):
        print("[+] Debugger break at PC=0x{:04X}".format(self.cpu.pc))
        self.cpu.debugger.stop(self.cpu)

    def close(self):
        self.screen.close()
