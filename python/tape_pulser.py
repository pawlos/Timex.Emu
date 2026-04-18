# ZX Spectrum tape pulse generator
# Converts .tap blocks into EAR-line edge transitions with T-state-accurate
# timing. Used by custom/turbo loaders that bypass the LD-BYTES ROM routine
# and poll port 0xFE bit 6 directly.


class TapePulser:
    PILOT_HALF = 2168
    PILOT_HEADER_PULSES = 8063
    PILOT_DATA_PULSES = 3223
    SYNC1 = 667
    SYNC2 = 735
    BIT0_HALF = 855
    BIT1_HALF = 1710
    PAUSE = 3_500_000  # ~1 s silence between blocks

    def __init__(self, tape):
        self._tape = tape
        self.playing = False
        self._level = 0
        self._schedule = []
        self._schedule_idx = 0
        self._cursor = 0
        self._t_base = 0
        self._pilot_count = 0

    def start(self, tstates):
        if self.playing:
            return
        self.playing = True
        self._t_base = tstates
        self._schedule = []
        self._schedule_idx = 0
        self._cursor = 0
        self._pilot_count = 0
        self._build_next_block()

    def stop(self):
        self.playing = False

    def read_ear(self, tstates):
        if not self.playing:
            return self._level
        rel = tstates - self._t_base
        while True:
            sched = self._schedule
            idx = self._schedule_idx
            while idx < len(sched) and sched[idx] <= rel:
                self._level ^= 1
                idx += 1
            self._schedule_idx = idx
            if idx < len(sched):
                break
            if not self._build_next_block():
                break
        return self._level

    def _pilot_pulses_emitted_for_debug(self):
        return self._pilot_count

    def _build_next_block(self):
        block = self._tape.next_block()
        if block is None:
            return False
        if self._schedule:
            self._cursor += self.PAUSE
        pilot = self.PILOT_HEADER_PULSES if block.flag < 128 else self.PILOT_DATA_PULSES
        for _ in range(pilot):
            self._cursor += self.PILOT_HALF
            self._schedule.append(self._cursor)
        self._pilot_count += pilot
        self._cursor += self.SYNC1
        self._schedule.append(self._cursor)
        self._cursor += self.SYNC2
        self._schedule.append(self._cursor)
        stream = bytes([block.flag]) + block.data + bytes([block.checksum])
        for b in stream:
            for i in range(7, -1, -1):
                pulse = self.BIT1_HALF if (b >> i) & 1 else self.BIT0_HALF
                self._cursor += pulse
                self._schedule.append(self._cursor)
                self._cursor += pulse
                self._schedule.append(self._cursor)
        return True
