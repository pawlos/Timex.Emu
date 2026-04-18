# ZX Spectrum 128K machine.
#
# Differences from the Timex 2048:
#   - Uses BankedRAM: 2 ROM banks x 16K + 8 RAM pages x 16K
#   - Port 0x7FFD writes drive paging (page / screen / ROM select + lock)
#   - CPU runs at 3.5469 MHz -> 70908 T-states per 1/50s frame
#   - Screen source can be page 5 (default) or shadow page 7
#   - No AY-3-8912 sound yet (step 4 will add it)

import os
import pygame

from cpu import CPU
from rom import ROM
from loggers import Logger
from screen import Screen, COLORS
from keyboard import Keyboard
from beeper import Beeper
from joystick import Joystick
from banked_ram import BankedRAM, PAGE_SIZE
from known_addresses import LD_BYTES
from tape import TapeFile
from tape_loader import TapeLoader
from tape_pulser import TapePulser, mix_ear_into_kb

TSTATES_PER_FRAME = 70908
DEFAULT_ROM = '../rom/128.rom'


class Spectrum128Machine:
    def __init__(self, cpu, ram, scale=2, debug=False,
                 tape_loader=None, tape_pulser=None):
        self.cpu = cpu
        self.ram = ram  # BankedRAM instance
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
        # Three distinct 128K ports share low byte 0xFD:
        #   0x7FFD (B=0x7F)  paging
        #   0xFFFD (B=0xFF)  AY-3-8912 register select
        #   0xBFFD (B=0xBF)  AY-3-8912 register data
        # The CPU's I/O layer dispatches on low byte only, so this handler
        # disambiguates by peeking at BC's high byte (cpu.B).
        cpu.io.on_write(0xFD, self._write_port_fd)

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

    def _write_port_fd(self, value):
        b = self.cpu.B
        if b == 0x7F:
            self.ram.write_port_7ffd(value)
            if self.debug:
                print("[7FFD <- 0x{:02X}] PC=0x{:04X} page={} rom={} scr={} lock={}".format(
                    value & 0xFF, self.cpu.pc,
                    self.ram.page_select, self.ram.rom_select,
                    self.ram.screen_select, self.ram.paging_locked))
        elif b == 0xFF:
            # AY register select — ignored until step 4 adds sound.
            pass
        elif b == 0xBF:
            # AY register data — ignored until step 4 adds sound.
            pass
        # Any other high byte: unknown peripheral at port NNFD — ignored.

    def _screen_bytes(self):
        return self.ram.current_screen

    def update(self):
        self.keyboard.handle_events(self.screen, self.joystick, self)
        self.screen.render(self._screen_bytes())
        self.beeper.render_audio()

    def _capture_snapshot(self):
        cpu = self.cpu
        ram = self.ram
        return (
            bytes(cpu.regs), bytes(cpu.regsPri),
            cpu.pc, cpu.sp, cpu.ix, cpu.iy,
            cpu.i, cpu.r, cpu.w, cpu.z,
            cpu.iff1, cpu.iff2, cpu.im, cpu.halted,
            tuple(bytes(p) for p in ram.pages),
            ram.rom_select, ram.page_select,
            ram.screen_select, ram.paging_locked,
        )

    def _restore_snapshot(self, snap):
        cpu = self.cpu
        ram = self.ram
        (regs, regsPri, pc, sp, ix, iy,
         i, r, w, z, iff1, iff2, im, halted,
         pages, rom_sel, page_sel, screen_sel, locked) = snap
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
        for idx, page in enumerate(pages):
            ram.pages[idx][:] = page
        ram.rom_select = rom_sel
        ram.page_select = page_sel
        ram.screen_select = screen_sel
        ram.paging_locked = locked

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
                    self.screen.render(self._screen_bytes())
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
                    title = "Spectrum 128 — {:.0f} FPS".format(fps)
                    if tape:
                        title += " — tape: {}".format(tape)
                    pygame.display.set_caption(title)
                    if self.debug:
                        print("PC=0x{:04X} iff1={} im={} page={} rom={} scr={}".format(
                            cpu.pc, cpu.iff1, cpu.im,
                            self.ram.page_select, self.ram.rom_select,
                            self.ram.screen_select))

    def reset(self):
        if self.tape_loader:
            self.cpu.debugger.setHook(LD_BYTES, None)
        self.cpu.reset()
        self.ram.clear()
        self.ram.rom_select = 0
        self.ram.page_select = 0
        self.ram.screen_select = 0
        self.ram.paging_locked = False
        if self.tape_loader:
            self.tape_loader.rewind()
            self.cpu.debugger.setHook(LD_BYTES, self.tape_loader.hook)
        print("[+] Reset")

    def save_state(self):
        # TODO: emit a 128K .z80 v3 snapshot in a later step.
        print("[!] save_state not implemented yet on Spectrum 128")

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


def _load_rom_banks(ram, rom_file):
    """Accept either a 32K combined file (bank0 then bank1) or a 16K file
    (bank 0 only). If `rom_file` is a path that has a sibling .1.rom next
    to it, that second file becomes bank 1."""
    with open(rom_file, 'rb') as f:
        data = f.read()
    if len(data) == PAGE_SIZE:
        ram.load_rom(0, data)
        sibling = rom_file.replace('.rom', '.1.rom')
        if sibling != rom_file and os.path.exists(sibling):
            with open(sibling, 'rb') as f:
                ram.load_rom(1, f.read())
    elif len(data) == 2 * PAGE_SIZE:
        ram.load_rom(0, data[:PAGE_SIZE])
        ram.load_rom(1, data[PAGE_SIZE:])
    else:
        raise ValueError(
            f"128K ROM file must be 16K or 32K, got {len(data)} bytes")


def factory(params, debugger):
    ram = BankedRAM()
    rom_file = params['rom_file'] or DEFAULT_ROM
    _load_rom_banks(ram, rom_file)

    if params['program'] is not None:
        # Load raw bytes at 0x8000 (the start of page 2 in the 128K map).
        with open(params['program'], 'rb') as f:
            data = f.read()
        ram.pages[2][:len(data)] = data

    cpu = CPU(debugger=debugger, rom=ROM(), ram=ram)
    if params['debugger']:
        cpu.logger = Logger(cpu)

    tape_loader = None
    tape_pulser = None
    if params['tape'] is not None:
        tape = TapeFile(params['tape'])
        if params['tape_mode'] == 'pulse':
            tape_pulser = TapePulser(tape)
        else:
            tape_loader = TapeLoader(tape)
            debugger.setHook(LD_BYTES, tape_loader.hook)

    if params['noDisplay']:
        return cpu, None

    machine = Spectrum128Machine(
        cpu, ram, scale=params['scale'], debug=params['debug'],
        tape_loader=tape_loader, tape_pulser=tape_pulser)

    if tape_pulser is not None:
        def _lazy_start(_cpu):
            tape_pulser.start(machine.global_tstates)
            return False
        debugger.setHook(LD_BYTES, _lazy_start)

    return cpu, machine
