# ZX Spectrum tape pulse generator
# Converts .tap blocks into EAR-line edge transitions with T-state-accurate
# timing. Used by custom/turbo loaders that bypass the LD-BYTES ROM routine
# and poll port 0xFE bit 6 directly.

EAR_BIT = 0x40


def mix_ear_into_kb(kb_byte, ear_bit):
    return (kb_byte & ~EAR_BIT) | ((ear_bit & 1) << 6)


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
        if self.playing and self._schedule_idx < len(self._schedule):
            return  # already streaming this block
        if self._schedule_idx < len(self._schedule):
            # Resume from stop: rebase t_base so the next scheduled edge
            # fires at the correct delta past tstates.
            last_rel = (self._schedule[self._schedule_idx - 1]
                        if self._schedule_idx > 0 else 0)
            self._t_base = tstates - last_rel
            self.playing = True
        else:
            # Fresh block — the previous one either finished or was never
            # started. Either way, pull the next block off the tape.
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
        sched = self._schedule
        idx = self._schedule_idx
        while idx < len(sched) and sched[idx] <= rel:
            self._level ^= 1
            idx += 1
        self._schedule_idx = idx
        # Once the current block's schedule is exhausted, stay silent until
        # the next explicit start() — this prevents idle keyboard polling
        # from silently advancing through the tape.
        return self._level

    def _pilot_pulses_emitted_for_debug(self):
        return self._pilot_count

    def block_info(self):
        tape = self._tape
        pos = getattr(tape, 'position', None)
        blocks = getattr(tape, 'blocks', None)
        if pos is None or blocks is None:
            return None, None
        return pos, len(blocks)

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
