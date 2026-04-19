import tests_suite

import unittest
from ay8910 import AY8910, AY_CLOCK


class tests_ay8910(unittest.TestCase):

    def test_default_registers_zero(self):
        ay = AY8910()
        for i in range(16):
            self.assertEqual(0, ay.regs[i])
        self.assertEqual(0, ay.selected)

    def test_reg_select_masks_to_4_bits(self):
        ay = AY8910()
        ay.write_reg_select(0x12)
        self.assertEqual(0x02, ay.selected)
        ay.write_reg_select(0xFF)
        self.assertEqual(0x0F, ay.selected)

    def test_reg_data_lands_in_selected(self):
        ay = AY8910()
        ay.write_reg_select(7)
        ay.write_reg_data(0xAA)
        self.assertEqual(0xAA, ay.regs[7])
        ay.write_reg_select(5)
        ay.write_reg_data(0x33)
        self.assertEqual(0x33, ay.regs[5])
        self.assertEqual(0xAA, ay.regs[7])  # previous reg untouched

    def test_read_returns_selected_reg(self):
        ay = AY8910()
        ay.write_reg_select(3)
        ay.write_reg_data(0x5C)
        self.assertEqual(0x5C, ay.read_reg())

    def test_silent_when_all_amps_zero(self):
        ay = AY8910()
        # Mixer enables all three tones (bits 0-2 = 0 = enabled), but
        # amplitudes are zero -> silence.
        ay.regs[7] = 0xF8
        samples = ay.render(200)
        for s in samples:
            self.assertEqual(0, s)

    def test_tone_a_produces_square_wave_at_expected_frequency(self):
        ay = AY8910(sample_rate=44100)
        # Channel A period = 100 (low byte), high 0. Frequency = AY_CLOCK / (16 * 100)
        ay.regs[0] = 100
        ay.regs[1] = 0
        ay.regs[7] = 0xFE   # tone A enabled, others muted
        ay.regs[8] = 15     # full amp A
        samples = ay.render(2000)
        # Count zero-crossings to estimate frequency.
        crossings = 0
        prev = samples[0]
        for s in samples[1:]:
            if (prev < 0 and s >= 0) or (prev >= 0 and s < 0):
                crossings += 1
            prev = s
        # Expected frequency: AY_CLOCK is first divided by 16, then by the
        # period counter, and the output flips on each terminal count —
        # giving a full cycle of 32 * period clocks.
        expected_hz = AY_CLOCK / (32 * 100)
        # Crossings per second = 2 * frequency (up + down per cycle)
        observed_hz = (crossings / 2) / (2000 / 44100)
        # Allow 5% tolerance
        self.assertAlmostEqual(expected_hz, observed_hz, delta=expected_hz * 0.05)

    def test_mixer_mute_silences_channel(self):
        ay = AY8910()
        ay.regs[0] = 100
        ay.regs[7] = 0xFF   # all tones muted (bits 0-2 all 1)
        ay.regs[8] = 15
        samples = ay.render(500)
        for s in samples:
            self.assertEqual(0, s)

    def test_channels_b_and_c_independent(self):
        ay = AY8910()
        # Channel C enabled with amp 10; A and B muted/silent.
        ay.regs[4] = 200
        ay.regs[5] = 0
        ay.regs[7] = 0b11111011   # only C enabled (bit 2 = 0)
        ay.regs[10] = 10
        samples = ay.render(1000)
        self.assertTrue(any(s != 0 for s in samples))
        # Bounded by level 10's entry in the volume table (both signs).
        from ay8910 import AY_VOLUME_TABLE
        peak = AY_VOLUME_TABLE[10]
        for s in samples:
            self.assertLessEqual(abs(s), peak)

    def test_zero_period_treated_as_one(self):
        # Period 0 should not divide by zero — treat as 1 for safety.
        ay = AY8910()
        ay.regs[0] = 0
        ay.regs[1] = 0
        ay.regs[7] = 0xFE
        ay.regs[8] = 15
        # Should not raise
        ay.render(100)

    def test_amplitude_is_logarithmic(self):
        # Each level ~ sqrt(2) louder than the previous. Ratio between
        # adjacent levels should increase, not be constant (linear).
        from ay8910 import AY_VOLUME_TABLE
        self.assertEqual(16, len(AY_VOLUME_TABLE))
        # Level 0 is silent, level 15 is loudest
        self.assertEqual(0, AY_VOLUME_TABLE[0])
        self.assertGreater(AY_VOLUME_TABLE[15], AY_VOLUME_TABLE[14])
        # Rough log check: level 15 should be >~40x level 1 for the log curve
        # (linear would put level 15 at only 15x level 1).
        self.assertGreater(
            AY_VOLUME_TABLE[15] / max(1, AY_VOLUME_TABLE[1]), 40)

    def test_noise_only_channel_produces_nonperiodic_output(self):
        # Tone A muted, noise A active, amp nonzero.
        ay = AY8910()
        ay.regs[6] = 10                 # noise period
        ay.regs[7] = 0b11110110         # tone A muted, noise A enabled
        ay.regs[8] = 15                 # full amp A
        samples = ay.render(4000)
        # Should not be all silent
        self.assertTrue(any(s != 0 for s in samples))
        # And not purely periodic at tone-channel rate — crude check is that
        # consecutive zero-crossing intervals vary (tone would be uniform).
        intervals = []
        prev_sign = 1 if samples[0] >= 0 else -1
        last = 0
        for i, s in enumerate(samples[1:], 1):
            sign = 1 if s >= 0 else -1
            if sign != prev_sign:
                intervals.append(i - last)
                last = i
                prev_sign = sign
        # At least some variability
        if len(intervals) > 4:
            unique = len(set(intervals))
            self.assertGreater(unique, 1)

    def test_writing_r13_resets_envelope(self):
        ay = AY8910()
        # Walk the envelope forward, then rewrite R13 — should restart.
        ay.regs[11] = 1     # short env period
        ay.write_reg_select(13)
        ay.write_reg_data(0x00)  # shape 0: decay, hold at 0
        # Run some samples to advance envelope
        ay.regs[8] = 0x10   # channel A uses envelope
        ay.regs[7] = 0xFE
        ay.render(500)
        mid_level = ay._env_level
        # Rewrite R13 — should reset to starting level (15 for decay)
        ay.write_reg_data(0x00)
        self.assertEqual(15, ay._env_level)
        self.assertFalse(ay._env_holding)

    def test_shape_0_decays_then_holds_at_zero(self):
        # Shape 0 = decay, CONT=0 -> hold at 0 forever.
        ay = AY8910()
        ay.regs[11] = 1     # fast envelope
        ay.regs[12] = 0
        ay.write_reg_select(13)
        ay.write_reg_data(0x00)
        # Run enough samples to guarantee the 32-step cycle completes.
        ay.render(10000)
        self.assertTrue(ay._env_holding)
        self.assertEqual(0, ay._env_level)

    def test_shape_12_repeats_attack(self):
        # Shape 12 = CONT=1, ATT=1, ALT=0, HOLD=0 -> repeating attack ////
        ay = AY8910()
        ay.regs[11] = 1
        ay.regs[12] = 0
        ay.write_reg_select(13)
        ay.write_reg_data(0x0C)
        ay.render(10000)
        # Must not be holding — repeats forever
        self.assertFalse(ay._env_holding)

    def test_shape_13_attack_then_hold_at_15(self):
        # Shape 13 = CONT=1, ATT=1, ALT=0, HOLD=1 -> /⎺⎺⎺
        ay = AY8910()
        ay.regs[11] = 1
        ay.regs[12] = 0
        ay.write_reg_select(13)
        ay.write_reg_data(0x0D)
        ay.render(10000)
        self.assertTrue(ay._env_holding)
        self.assertEqual(15, ay._env_level)

    def test_channel_amp_bit_4_uses_envelope_level(self):
        # Channel A set to envelope mode; with envelope > 0 the channel
        # should produce non-silent output even though R8 low nibble = 0.
        ay = AY8910()
        ay.regs[0] = 100
        ay.regs[7] = 0xFE       # tone A enabled
        ay.regs[8] = 0x10       # envelope mode, low nibble 0
        ay.regs[11] = 1
        ay.regs[12] = 0
        ay.write_reg_select(13)
        ay.write_reg_data(0x0D)  # hold at 15
        samples = ay.render(3000)
        self.assertTrue(any(s != 0 for s in samples))

    def test_both_tone_and_noise_muted_is_silent(self):
        ay = AY8910()
        ay.regs[0] = 100
        ay.regs[6] = 10
        ay.regs[7] = 0b11111111   # tone + noise muted everywhere
        ay.regs[8] = 15
        samples = ay.render(500)
        for s in samples:
            self.assertEqual(0, s)


if __name__ == '__main__':
    unittest.main()
