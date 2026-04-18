import tests_suite

import unittest
from tape import TapeBlock
from tape_pulser import TapePulser


class FakeTape:
    def __init__(self, blocks):
        self.blocks = list(blocks)
        self._pos = 0

    def next_block(self):
        if self._pos >= len(self.blocks):
            return None
        b = self.blocks[self._pos]
        self._pos += 1
        return b


def _block(flag, data):
    checksum = flag
    for b in data:
        checksum ^= b
    return TapeBlock(flag, bytes(data), checksum)


class tests_tape_pulser(unittest.TestCase):

    def test_silent_before_start(self):
        pulser = TapePulser(FakeTape([_block(0xFF, [0x00])]))
        self.assertEqual(0, pulser.read_ear(0))
        self.assertEqual(0, pulser.read_ear(10_000_000))

    def test_pilot_toggles_every_2168_tstates(self):
        pulser = TapePulser(FakeTape([_block(0xFF, [0x00])]))
        pulser.start(0)
        # First edge at T=2168 takes level from 0 -> 1
        self.assertEqual(0, pulser.read_ear(2167))
        self.assertEqual(1, pulser.read_ear(2168))
        # Next edge at T=4336: 1 -> 0
        self.assertEqual(1, pulser.read_ear(4335))
        self.assertEqual(0, pulser.read_ear(4336))
        # And again
        self.assertEqual(1, pulser.read_ear(6504))

    def test_pilot_length_header_vs_data(self):
        # Header block: flag < 128, 8063 pilot pulses
        header = TapePulser(FakeTape([_block(0x00, [0x01])]))
        header.start(0)
        self.assertEqual(TapePulser.PILOT_HEADER_PULSES, header._pilot_pulses_emitted_for_debug())
        # Data block: flag >= 128, 3223 pilot pulses
        data = TapePulser(FakeTape([_block(0xFF, [0x01])]))
        data.start(0)
        self.assertEqual(TapePulser.PILOT_DATA_PULSES, data._pilot_pulses_emitted_for_debug())

    def test_sync_pulses_after_pilot(self):
        pulser = TapePulser(FakeTape([_block(0xFF, [0x00])]))
        pulser.start(0)
        pilot_end = TapePulser.PILOT_DATA_PULSES * TapePulser.PILOT_HALF
        sync1_end = pilot_end + TapePulser.SYNC1
        sync2_end = sync1_end + TapePulser.SYNC2
        # Level at end of pilot (after last pilot toggle)
        level_at_pilot_end = pulser.read_ear(pilot_end)
        # Sync1 toggles once
        self.assertNotEqual(level_at_pilot_end, pulser.read_ear(sync1_end))
        # Sync2 toggles back
        self.assertEqual(level_at_pilot_end, pulser.read_ear(sync2_end))

    def test_bit_pulses_zero_vs_one(self):
        # Single-byte block where we control exactly one bit pattern.
        # Byte 0x80 = 1,0,0,0,0,0,0,0 (MSB first).
        # Pulser stream will be: flag(0xFF) + data(0x80) + checksum(0x7F)
        # Simpler: use a header block with flag=0x00 and data=[0x80]
        # stream = 0x00, 0x80, 0x80 (xor of 0x00 and 0x80)
        pulser = TapePulser(FakeTape([_block(0x00, [0x80])]))
        pulser.start(0)
        # Skip to start of data stream
        t_data = (TapePulser.PILOT_HEADER_PULSES * TapePulser.PILOT_HALF
                  + TapePulser.SYNC1 + TapePulser.SYNC2)
        # First byte is the flag 0x00 = all zeros
        # Each zero-bit uses BIT0_HALF = 855, two pulses each, so one bit = 1710
        for bit_idx in range(8):
            before = pulser.read_ear(t_data + bit_idx * 2 * TapePulser.BIT0_HALF)
            after_half = pulser.read_ear(
                t_data + bit_idx * 2 * TapePulser.BIT0_HALF + TapePulser.BIT0_HALF)
            after_full = pulser.read_ear(
                t_data + bit_idx * 2 * TapePulser.BIT0_HALF + 2 * TapePulser.BIT0_HALF)
            # One full bit = two toggles, ending with same level as before
            self.assertNotEqual(before, after_half)
            self.assertEqual(before, after_full)

        # Second byte is data 0x80 = 1,0,0,0,0,0,0,0
        t_second_byte = t_data + 8 * 2 * TapePulser.BIT0_HALF
        # First bit of 0x80 is 1: uses BIT1_HALF = 1710 per pulse
        before = pulser.read_ear(t_second_byte)
        after_half = pulser.read_ear(t_second_byte + TapePulser.BIT1_HALF)
        after_full = pulser.read_ear(t_second_byte + 2 * TapePulser.BIT1_HALF)
        self.assertNotEqual(before, after_half)
        self.assertEqual(before, after_full)

    def test_stop_freezes_level(self):
        pulser = TapePulser(FakeTape([_block(0xFF, [0x00])]))
        pulser.start(0)
        level_before_stop = pulser.read_ear(2168)  # after first pilot edge
        pulser.stop()
        # Time passes; level should not change
        self.assertEqual(level_before_stop, pulser.read_ear(10_000_000))

    def test_restart_resumes_from_last_level(self):
        # Not strictly required — document behaviour:
        # After stop() + start(t), pulser continues building from current
        # position, but clock resets so first edge is t + PILOT_HALF from
        # the restart point.
        pulser = TapePulser(FakeTape([_block(0xFF, [0x00])]))
        pulser.start(0)
        pulser.read_ear(10_000)
        pulser.stop()
        frozen = pulser.read_ear(100_000)
        pulser.start(200_000)
        # Level should still be `frozen` immediately after restart
        self.assertEqual(frozen, pulser.read_ear(200_000))


if __name__ == '__main__':
    unittest.main()
