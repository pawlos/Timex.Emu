# AY-3-8912 programmable sound generator — ZX Spectrum 128 variant.
#
# On the 128K, the AY runs at CPU/2 = ~1.7735 MHz. It has 16 registers
# accessed through two ports that share the same low byte (0xFD):
#   0xFFFD (B=0xFF) — register select
#   0xBFFD (B=0xBF) — data for the selected register
#
# Implemented here: three tone channels, the mixer, per-channel amplitude
# on a logarithmic scale, and a 17-bit LFSR noise generator. Envelope
# generator is not yet modeled (channel amp bit 4 "use envelope" falls
# back to fixed-level behaviour for now).

import array

AY_CLOCK = 1773500
NUM_REGS = 16

# Logarithmic amplitude table (16 steps, ~3 dB per step), scaled so that
# three channels summed peak near ±32767. Numbers come from the common
# MAME-style AY volume curve, divided by 6 so 3-channel peak fits signed
# 16-bit.
_RAW_AY = [
    0x0000, 0x0385, 0x053D, 0x0770,
    0x0A45, 0x0F40, 0x1510, 0x227E,
    0x289F, 0x414E, 0x5B21, 0x7258,
    0x905E, 0xB550, 0xD7A0, 0xFFFF,
]
AY_VOLUME_TABLE = tuple(v // 6 for v in _RAW_AY)


class AY8910:
    def __init__(self, sample_rate=44100):
        self.regs = bytearray(NUM_REGS)
        self.selected = 0
        self.sample_rate = sample_rate
        self._phase = [0.0, 0.0, 0.0]
        self._output = [0, 0, 0]
        self._noise_phase = 0.0
        self._noise_output = 1
        self._lfsr = 1  # 17-bit; must be non-zero

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

    def _noise_period(self):
        p = self.regs[6] & 0x1F
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
        # For each channel, is tone or noise routed to output?
        # Mixer bits: 0..2 = tone A/B/C mute (1 = muted), 3..5 = noise mute.
        tone_on0 = (mixer & 0x01) == 0
        tone_on1 = (mixer & 0x02) == 0
        tone_on2 = (mixer & 0x04) == 0
        noise_on0 = (mixer & 0x08) == 0
        noise_on1 = (mixer & 0x10) == 0
        noise_on2 = (mixer & 0x20) == 0
        # If both tone and noise are muted on a channel, it contributes DC
        # only — we treat that as silent in AC output.
        active0 = tone_on0 or noise_on0
        active1 = tone_on1 or noise_on1
        active2 = tone_on2 or noise_on2
        if not (active0 or active1 or active2):
            return out

        t0 = 16 * self._tone_period(0)
        t1 = 16 * self._tone_period(1)
        t2 = 16 * self._tone_period(2)
        tn = 16 * self._noise_period()
        ticks = AY_CLOCK / self.sample_rate

        ph = self._phase
        o = self._output
        lev0 = AY_VOLUME_TABLE[a0]
        lev1 = AY_VOLUME_TABLE[a1]
        lev2 = AY_VOLUME_TABLE[a2]
        lfsr = self._lfsr
        noise_phase = self._noise_phase
        noise_bit = self._noise_output

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
            noise_phase += ticks
            if noise_phase >= tn:
                noise_phase -= tn
                # 17-bit LFSR, taps at bits 0 and 3
                feedback = (lfsr ^ (lfsr >> 3)) & 1
                lfsr = ((lfsr >> 1) | (feedback << 16)) & 0x1FFFF
                noise_bit = lfsr & 1

            total = 0
            # Per-channel mix: output = (tone OR !tone_on) AND (noise OR !noise_on)
            # encoded equivalently as: t_eff = tone_bit if tone_on else 1,
            #                          n_eff = noise_bit if noise_on else 1,
            #                          bit  = t_eff & n_eff.
            if active0:
                t_eff = o[0] if tone_on0 else 1
                n_eff = noise_bit if noise_on0 else 1
                total += lev0 if (t_eff & n_eff) else -lev0
            if active1:
                t_eff = o[1] if tone_on1 else 1
                n_eff = noise_bit if noise_on1 else 1
                total += lev1 if (t_eff & n_eff) else -lev1
            if active2:
                t_eff = o[2] if tone_on2 else 1
                n_eff = noise_bit if noise_on2 else 1
                total += lev2 if (t_eff & n_eff) else -lev2

            if total > 32767:
                total = 32767
            elif total < -32767:
                total = -32767
            out[i] = total

        self._lfsr = lfsr
        self._noise_phase = noise_phase
        self._noise_output = noise_bit
        return out
