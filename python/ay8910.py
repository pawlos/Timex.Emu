# AY-3-8912 programmable sound generator — ZX Spectrum 128 variant.
#
# On the 128K, the AY runs at CPU/2 = ~1.7735 MHz. It has 16 registers
# accessed through two ports that share the same low byte (0xFD):
#   0xFFFD (B=0xFF) — register select
#   0xBFFD (B=0xBF) — data for the selected register
#
# Implemented here: three tone channels, the mixer, per-channel amplitude
# on a logarithmic scale, a 17-bit LFSR noise generator, and the envelope
# generator (all 16 shapes, 32-step level cycle, period from R11/R12).

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
        # Envelope generator state
        self._env_phase = 0.0
        self._env_level = 0
        self._env_attacking = False
        self._env_holding = False

    def write_reg_select(self, value):
        self.selected = value & 0x0F

    def write_reg_data(self, value):
        v = value & 0xFF
        self.regs[self.selected] = v
        # Writing R13 — including rewriting the same value — resets the
        # envelope. Games use this to retrigger a note.
        if self.selected == 13:
            self._envelope_reset()

    def read_reg(self):
        return self.regs[self.selected]

    def _envelope_reset(self):
        shape = self.regs[13] & 0x0F
        # ATT bit (bit 2): 1 = attack phase first, 0 = decay
        attacking = (shape & 0x04) != 0
        self._env_attacking = attacking
        self._env_level = 0 if attacking else 15
        self._env_holding = False

    def _envelope_tick(self):
        if self._env_holding:
            return
        if self._env_attacking:
            self._env_level += 1
        else:
            self._env_level -= 1
        if 0 <= self._env_level <= 15:
            return
        # End of a 32-step cycle — decide next behaviour from shape bits.
        shape = self.regs[13] & 0x0F
        cont = (shape & 0x08) != 0
        alt = (shape & 0x02) != 0
        hold = (shape & 0x01) != 0
        if not cont:
            # Shapes 0..7: hold at 0 after first cycle.
            self._env_level = 0
            self._env_holding = True
            return
        if hold:
            # Shapes 9,11,13,15: freeze at end-of-cycle level, inverted if ALT.
            endpoint = 15 if self._env_attacking else 0
            self._env_level = (15 - endpoint) if alt else endpoint
            self._env_holding = True
            return
        if alt:
            # Shapes 10, 14: flip direction, stay at boundary level.
            self._env_attacking = not self._env_attacking
            self._env_level = 15 if not self._env_attacking else 0
        else:
            # Shapes 8, 12: same direction, reset to start boundary.
            self._env_level = 0 if self._env_attacking else 15

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
        r8, r9, r10 = self.regs[8], self.regs[9], self.regs[10]
        a0_fixed = r8 & 0x0F
        a1_fixed = r9 & 0x0F
        a2_fixed = r10 & 0x0F
        env0 = (r8 & 0x10) != 0
        env1 = (r9 & 0x10) != 0
        env2 = (r10 & 0x10) != 0
        # If no channel would produce audible amplitude we can skip the
        # sample loop, but we must still advance the envelope clock so its
        # state (level, holding) keeps up with real time. That way a
        # channel that flips to envelope mode later sees a plausible
        # envelope position.
        silent = (not env0 and not env1 and not env2 and
                  a0_fixed == 0 and a1_fixed == 0 and a2_fixed == 0)
        if silent:
            env_period = self.regs[11] | (self.regs[12] << 8)
            if env_period == 0:
                env_period = 1
            te = 256 * env_period
            ticks_total = (AY_CLOCK / self.sample_rate) * num_samples
            self._env_phase += ticks_total
            while self._env_phase >= te:
                self._env_phase -= te
                self._envelope_tick()
            return out

        mixer = self.regs[7]
        tone_on0 = (mixer & 0x01) == 0
        tone_on1 = (mixer & 0x02) == 0
        tone_on2 = (mixer & 0x04) == 0
        noise_on0 = (mixer & 0x08) == 0
        noise_on1 = (mixer & 0x10) == 0
        noise_on2 = (mixer & 0x20) == 0
        active0 = tone_on0 or noise_on0
        active1 = tone_on1 or noise_on1
        active2 = tone_on2 or noise_on2
        if not (active0 or active1 or active2):
            return out

        t0 = 16 * self._tone_period(0)
        t1 = 16 * self._tone_period(1)
        t2 = 16 * self._tone_period(2)
        tn = 16 * self._noise_period()
        # Envelope period = R11 | (R12 << 8); clock is AY_CLOCK / 256, so a
        # single envelope step takes 256 * env_period AY clocks.
        env_period = self.regs[11] | (self.regs[12] << 8)
        if env_period == 0:
            env_period = 1
        te = 256 * env_period
        ticks = AY_CLOCK / self.sample_rate

        ph = self._phase
        o = self._output
        fix0 = AY_VOLUME_TABLE[a0_fixed]
        fix1 = AY_VOLUME_TABLE[a1_fixed]
        fix2 = AY_VOLUME_TABLE[a2_fixed]
        lfsr = self._lfsr
        noise_phase = self._noise_phase
        noise_bit = self._noise_output
        env_phase = self._env_phase

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
                feedback = (lfsr ^ (lfsr >> 3)) & 1
                lfsr = ((lfsr >> 1) | (feedback << 16)) & 0x1FFFF
                noise_bit = lfsr & 1
            env_phase += ticks
            if env_phase >= te:
                env_phase -= te
                self._envelope_tick()
            env_lev = AY_VOLUME_TABLE[self._env_level]

            total = 0
            if active0:
                t_eff = o[0] if tone_on0 else 1
                n_eff = noise_bit if noise_on0 else 1
                lev = env_lev if env0 else fix0
                total += lev if (t_eff & n_eff) else -lev
            if active1:
                t_eff = o[1] if tone_on1 else 1
                n_eff = noise_bit if noise_on1 else 1
                lev = env_lev if env1 else fix1
                total += lev if (t_eff & n_eff) else -lev
            if active2:
                t_eff = o[2] if tone_on2 else 1
                n_eff = noise_bit if noise_on2 else 1
                lev = env_lev if env2 else fix2
                total += lev if (t_eff & n_eff) else -lev

            if total > 32767:
                total = 32767
            elif total < -32767:
                total = -32767
            out[i] = total

        self._lfsr = lfsr
        self._noise_phase = noise_phase
        self._noise_output = noise_bit
        self._env_phase = env_phase
        return out
