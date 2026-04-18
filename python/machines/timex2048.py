# Timex Computer 2048 — 48K flat-RAM machine.

import pygame

from cpu import CPU
from rom import ROM
from ram import RAM
from loggers import Logger
from screen import Screen, COLORS
from keyboard import Keyboard
from beeper import Beeper
from joystick import Joystick
from snapshot import save_z80
from known_addresses import LD_BYTES
from tape import TapeFile
from tape_loader import TapeLoader
from tape_pulser import TapePulser, mix_ear_into_kb
from opcodes import Opcodes

TSTATES_PER_FRAME = 69888
DEFAULT_ROM = '../rom/tc2048.rom'


def _system_error(cpu):
    print('System error')
    Opcodes.hlt(cpu, 0x76, cpu.logger)
    return True


def _system_print_char(cpu):
    print(chr(cpu.A), end='')
    Opcodes.ret(cpu, 0xC9, cpu.logger)
    return True


class Timex2048Machine:
    def __init__(self, cpu, scale=2, debug=False, rom=None,
                 tape_loader=None, tape_pulser=None):
        self.cpu = cpu
        self.rom = rom
        self.tape_loader = tape_loader
        self.tape_pulser = tape_pulser
        self.screen = Screen(scale)
        self.keyboard = Keyboard()
        self.beeper = Beeper()
        self.joystick = Joystick()
        self.debug = debug
        self.paused = False
        self.turbo = False
        self.rewinding = False
        self._rewind_buffer = []
        self._rewind_max = 500
        self._rewind_interval = 5

        cpu.io.on_read(0xFE, self._read_port_fe)
        cpu.io.on_read(0x1F, self.joystick.read)
        cpu.io.on_write(0xFE, self._write_port_fe)

        if tape_loader:
            tape_loader.machine = self

        self._frame_count = 0
        self._clock = pygame.time.Clock()
        self._last_tape_status = None

    @property
    def global_tstates(self):
        return self._frame_count * TSTATES_PER_FRAME + self.cpu.tstates

    def _read_port_fe(self, high_byte=0):
        value = self.keyboard.read(high_byte)
        if self.tape_pulser is not None:
            value = mix_ear_into_kb(
                value, self.tape_pulser.read_ear(self.global_tstates))
        return value

    def _write_port_fe(self, value):
        self.screen.set_border(value & 0x07)
        self.beeper.set_speaker((value >> 4) & 1, self.cpu.tstates)

    def update(self):
        self.keyboard.handle_events(self.screen, self.joystick, self)
        self.screen.render(self.cpu.ram)
        self.beeper.render_audio()

    def _capture_snapshot(self):
        cpu = self.cpu
        return (
            bytes(cpu.regs), bytes(cpu.regsPri),
            cpu.pc, cpu.sp, cpu.ix, cpu.iy,
            cpu.i, cpu.r, cpu.w, cpu.z,
            cpu.iff1, cpu.iff2, cpu.im, cpu.halted,
            bytes(cpu.ram.ram)
        )

    def _restore_snapshot(self, snap):
        cpu = self.cpu
        (regs, regsPri, pc, sp, ix, iy,
         i, r, w, z, iff1, iff2, im, halted, ram) = snap
        cpu.regs[:] = regs
        cpu.regsPri[:] = regsPri
        cpu.pc = pc
        cpu.sp = sp
        cpu.ix = ix
        cpu.iy = iy
        cpu.i = i
        cpu.r = r
        cpu.w = w
        cpu.z = z
        cpu.iff1 = iff1
        cpu.iff2 = iff2
        cpu.im = im
        cpu.halted = halted
        cpu.ram.ram[:] = ram

    def run(self, pc=0x0):
        cpu = self.cpu
        cpu.pc = pc
        while True:
            if self.paused:
                self.keyboard.handle_events(self.screen, self.joystick, self)
                self._clock.tick(50)
                continue
            if self.rewinding:
                self.keyboard.handle_events(self.screen, self.joystick, self)
                if self._rewind_buffer:
                    self._restore_snapshot(self._rewind_buffer.pop())
                    self.screen.render(cpu.ram)
                    self._clock.tick(50)
                else:
                    self.rewinding = False
                continue
            if not cpu.halted:
                cpu.readOp()
            else:
                cpu.m_cycles, cpu.t_states = 1, 4
            cpu._checkInterrupts()
            if cpu.tstates >= TSTATES_PER_FRAME:
                cpu.tstates -= TSTATES_PER_FRAME
                cpu._interruptPending = True
                if self._frame_count % self._rewind_interval == 0:
                    self._rewind_buffer.append(self._capture_snapshot())
                    if len(self._rewind_buffer) > self._rewind_max:
                        self._rewind_buffer.pop(0)
                if self.turbo and self._frame_count % 10 != 0:
                    self.keyboard.handle_events(self.screen, self.joystick, self)
                else:
                    self.update()
                    if not self.turbo:
                        self._clock.tick(50)
                self._frame_count += 1
                tape = self._tape_status()
                if tape != self._last_tape_status:
                    if tape is not None:
                        print("[+] Tape: {}".format(tape))
                    self._last_tape_status = tape
                if self._frame_count % 50 == 0:
                    fps = self._clock.get_fps()
                    title = "Timex 2048 — {:.0f} FPS".format(fps)
                    if tape:
                        title += " — tape: {}".format(tape)
                    pygame.display.set_caption(title)
                    if self.debug:
                        print("PC=0x{:04X} iff1={} im={} IY=0x{:04X}".format(
                            cpu.pc, cpu.iff1, cpu.im, cpu.IY))

    def reset(self):
        if self.tape_loader:
            self.cpu.debugger.setHook(LD_BYTES, None)
        self.cpu.reset()
        self.cpu.ram.clear()
        if self.rom:
            self.cpu.ram.load(self.rom)
        if self.tape_loader:
            self.tape_loader.rewind()
            self.cpu.debugger.setHook(LD_BYTES, self.tape_loader.hook)
        print("[+] Reset")

    def save_state(self):
        import time
        filename = "state_{}.z80".format(int(time.time()))
        border_idx = next((i for i, c in enumerate(COLORS) if c == self.screen.border_color), 7)
        save_z80(filename, self.cpu, border_idx)

    def _tape_status(self):
        if self.tape_loader:
            return "play" if self.tape_loader.playing else "stop"
        if self.tape_pulser is not None:
            pos, total = self.tape_pulser.block_info()
            counter = " [{}/{}]".format(pos, total) if total else ""
            if not self.tape_pulser.playing:
                return "stop" + counter
            if self.tape_pulser._schedule_idx < len(self.tape_pulser._schedule):
                return "streaming" + counter
            return "done — F6 for next" + counter
        return None

    def toggle_tape(self):
        if self.tape_loader:
            self.tape_loader.toggle_play()
        elif self.tape_pulser is not None:
            if self.tape_pulser.playing:
                self.tape_pulser.stop()
                print("[+] Tape: STOP")
            else:
                self.tape_pulser.start(self.global_tstates)
                print("[+] Tape: PLAY")

    def enter_debugger(self):
        print("[+] Debugger break at PC=0x{:04X}".format(self.cpu.pc))
        self.cpu.debugger.stop(self.cpu)

    def close(self):
        self.screen.close()


def factory(params, debugger):
    if params['mapAt'] != 0x0:
        rom = ROM(mapAt=params['mapAt'])
    else:
        rom = ROM()
    if params['rom_file'] is None:
        rom.loadFrom(DEFAULT_ROM)
    else:
        rom.loadFrom(params['rom_file'], False)

    ram = RAM()
    if params['program'] is not None:
        ram.loadProgramAt(params['program'], 0x8000)

    if params['hookSystem']:
        debugger.setHook(0x08, _system_error)
        debugger.setHook(0x10, _system_print_char)

    tape_loader = None
    tape_pulser = None
    if params['tape'] is not None:
        tape = TapeFile(params['tape'])
        if params['tape_mode'] == 'pulse':
            tape_pulser = TapePulser(tape)
        else:
            tape_loader = TapeLoader(tape)
            debugger.setHook(LD_BYTES, tape_loader.hook)

    cpu = CPU(debugger=debugger, rom=rom, ram=ram)
    if params['debugger']:
        cpu.logger = Logger(cpu)

    if params['noDisplay']:
        return cpu, None

    machine = Timex2048Machine(
        cpu, scale=params['scale'], debug=params['debug'],
        rom=rom, tape_loader=tape_loader, tape_pulser=tape_pulser)

    if tape_pulser is not None:
        def _lazy_start(_cpu):
            tape_pulser.start(machine.global_tstates)
            return False
        debugger.setHook(LD_BYTES, _lazy_start)

    return cpu, machine
