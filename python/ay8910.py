# AY-3-8912 programmable sound generator — ZX Spectrum 128 variant.
#
# On the 128K, the AY runs at CPU/2 = ~1.7735 MHz. It has 16 registers
# accessed through two ports that share the same low byte (0xFD):
#   0xFFFD (B=0xFF) — register select
#   0xBFFD (B=0xBF) — data for the selected register
#
# Implemented here: three tone channels with the mixer and per-channel
# amplitude. Noise generator, envelope generator, and I/O port registers
# are parsed but currently ignored — good enough for a lot of game music
# and can be enriched later.

import array

AY_CLOCK = 1773500
NUM_REGS = 16
VOL_SCALE = 700  # per amplitude step; 3 channels × 15 × 700 ~ within 16-bit


class AY8910:
    def __init__(self, sample_rate=44100):
        self.regs = bytearray(NUM_REGS)
        self.selected = 0
        self.sample_rate = sample_rate
        self._phase = [0.0, 0.0, 0.0]
        self._output = [0, 0, 0]

    def write_reg_select(self, value):
        self.selected = value & 0x0F

    def write_reg_data(self, value):
        self.regs[self.selected] = value & 0xFF

    def read_reg(self):
        return self.regs[self.selected]

    def _tone_period(self, channel):
        low = self.regs[channel * 2]
        high = self.regs[channel * 2 + 1] & 0x0F
        p = (high << 8) | low
        return p if p > 0 else 1

    def render(self, num_samples):
        """Return num_samples of signed-16 mono PCM at self.sample_rate."""
        out = array.array('h', [0] * num_samples)
        a0 = self.regs[8] & 0x0F
        a1 = self.regs[9] & 0x0F
        a2 = self.regs[10] & 0x0F
        if a0 == 0 and a1 == 0 and a2 == 0:
            return out

        mixer = self.regs[7]
        # tone_on[c] = True when the mixer lets tone pass (bit c = 0).
        tone_on = [(mixer >> c) & 1 == 0 for c in range(3)]

        t0 = 16 * self._tone_period(0)
        t1 = 16 * self._tone_period(1)
        t2 = 16 * self._tone_period(2)
        ticks = AY_CLOCK / self.sample_rate

        ph = self._phase
        o = self._output
        scale0 = a0 * VOL_SCALE
        scale1 = a1 * VOL_SCALE
        scale2 = a2 * VOL_SCALE
        on0, on1, on2 = tone_on

        for i in range(num_samples):
            ph[0] += ticks
            if ph[0] >= t0:
                o[0] ^= 1
                ph[0] -= t0
            ph[1] += ticks
            if ph[1] >= t1:
                o[1] ^= 1
                ph[1] -= t1
            ph[2] += ticks
            if ph[2] >= t2:
                o[2] ^= 1
                ph[2] -= t2

            total = 0
            if on0:
                total += scale0 if o[0] else -scale0
            if on1:
                total += scale1 if o[1] else -scale1
            if on2:
                total += scale2 if o[2] else -scale2
            if total > 32767:
                total = 32767
            elif total < -32767:
                total = -32767
            out[i] = total

        return out
