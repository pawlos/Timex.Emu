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
        # Should be non-silent
        self.assertTrue(any(s != 0 for s in samples))
        # And bounded by 10 * VOL_SCALE (both signs)
        from ay8910 import VOL_SCALE
        peak = 10 * VOL_SCALE
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


if __name__ == '__main__':
    unittest.main()
