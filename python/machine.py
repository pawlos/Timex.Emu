# Timex 2048 / ZX Spectrum Machine
# Coordinates CPU, screen, keyboard, beeper, and joystick

import pygame
from screen import Screen
from keyboard import Keyboard
from beeper import Beeper
from joystick import Joystick

TSTATES_PER_FRAME = 69888


class Machine:
    def __init__(self, cpu, scale=2):
        self.cpu = cpu
        self.screen = Screen(scale)
        self.keyboard = Keyboard()
        self.beeper = Beeper()
        self.joystick = Joystick()

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
        self.keyboard.handle_events(self.screen, self.joystick)
        self.screen.render(self.cpu.ram)
        self.beeper.render_audio()

    def run(self, pc=0x0):
        cpu = self.cpu
        cpu.pc = pc
        while True:
            if not cpu.halted:
                cpu.readOp()
            else:
                cpu.m_cycles, cpu.t_states = 1, 4
            cpu._checkInterrupts()
            if cpu.tstates >= TSTATES_PER_FRAME:
                cpu.tstates -= TSTATES_PER_FRAME
                cpu._interruptPending = True
                self.update()
                self._clock.tick(50)
                self._frame_count += 1
                if self._frame_count % 50 == 0:
                    print("PC=0x{:04X} iff1={} im={} IY=0x{:04X}".format(
                        cpu.pc, cpu.iff1, cpu.im, cpu.IY))

    def close(self):
        self.screen.close()
