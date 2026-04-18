import tests_suite

import os
import tempfile
import unittest

from banked_ram import BankedRAM
from cpu import CPU
from rom import ROM
from snapshot import load_z80


def _build_z80_v3_128k(port_7ffd=0x00, pc=0xC000, a=0x11, f=0x22,
                      hw_mode=4, pages=None):
    """Build a minimal v3 128K .z80 byte-stream.
    `pages` is a dict {page_num: bytes_16k}. Missing banks default to 0xFF fill.
    """
    header = bytearray(30 + 2 + 54)  # 30 base + 2 extra_len + 54 extra
    header[0] = a
    header[1] = f
    # PC in base header = 0 signals v2/v3
    header[6] = 0
    header[7] = 0
    header[8] = 0x00       # SP
    header[9] = 0x80
    header[12] = 0x07 << 1  # border=7 (just picks a non-zero value)
    # Extra header
    header[30] = 54 & 0xFF
    header[31] = 54 >> 8
    header[32] = pc & 0xFF
    header[33] = (pc >> 8) & 0xFF
    header[34] = hw_mode   # 4 = 128K for v3
    header[35] = port_7ffd  # port 0x7FFD latch value

    stream = bytes(header)
    if pages is None:
        pages = {p: bytes([0xFF]) * 16384 for p in range(3, 11)}
    for page_num, data in pages.items():
        assert len(data) == 16384
        # 0xFFFF length = uncompressed 16K
        stream += bytes([0xFF, 0xFF, page_num]) + data
    return stream


class tests_snapshot_128k(unittest.TestCase):

    def _make_cpu_banked(self):
        ram = BankedRAM()
        cpu = CPU(rom=ROM(), ram=ram)
        return cpu, ram

    def test_v3_128k_pages_land_in_banks_0_to_7(self):
        cpu, ram = self._make_cpu_banked()
        pages = {pnum: bytes([pnum - 3] * 16384) for pnum in range(3, 11)}
        data = _build_z80_v3_128k(pages=pages)
        with tempfile.NamedTemporaryFile(suffix='.z80', delete=False) as f:
            f.write(data)
            fn = f.name
        try:
            load_z80(fn, cpu)
            # Page N in .z80 -> bank (N-3) in BankedRAM
            for bank in range(8):
                self.assertEqual(bank, ram.pages[bank][0])
                self.assertEqual(bank, ram.pages[bank][16383])
        finally:
            os.unlink(fn)

    def test_v3_128k_applies_port_7ffd(self):
        cpu, ram = self._make_cpu_banked()
        data = _build_z80_v3_128k(port_7ffd=0x17)  # page=7, scr=0, rom=1
        with tempfile.NamedTemporaryFile(suffix='.z80', delete=False) as f:
            f.write(data)
            fn = f.name
        try:
            load_z80(fn, cpu)
            self.assertEqual(7, ram.page_select)
            self.assertEqual(0, ram.screen_select)
            self.assertEqual(1, ram.rom_select)
        finally:
            os.unlink(fn)

    def test_v3_128k_shadow_screen_select(self):
        cpu, ram = self._make_cpu_banked()
        data = _build_z80_v3_128k(port_7ffd=0x08)  # scr=1
        with tempfile.NamedTemporaryFile(suffix='.z80', delete=False) as f:
            f.write(data)
            fn = f.name
        try:
            load_z80(fn, cpu)
            self.assertEqual(1, ram.screen_select)
        finally:
            os.unlink(fn)

    def test_v3_128k_sets_cpu_state(self):
        cpu, ram = self._make_cpu_banked()
        data = _build_z80_v3_128k(pc=0xABCD, a=0x77, f=0x88)
        with tempfile.NamedTemporaryFile(suffix='.z80', delete=False) as f:
            f.write(data)
            fn = f.name
        try:
            load_z80(fn, cpu)
            self.assertEqual(0xABCD, cpu.pc)
            self.assertEqual(0x77, cpu.A)
            self.assertEqual(0x88, cpu.F)
        finally:
            os.unlink(fn)

    def test_v2_128k_hw_mode_3(self):
        # v2 uses extra_len=23 and hw_mode=3 for 128K (different from v3).
        cpu, ram = self._make_cpu_banked()
        header = bytearray(30 + 2 + 23)
        header[6] = 0
        header[7] = 0
        header[30] = 23
        header[31] = 0
        header[32] = 0x00   # PC
        header[33] = 0x40
        header[34] = 3      # 128K in v2
        header[35] = 0x05   # page_select=5
        stream = bytes(header)
        # Supply all 8 pages
        for page_num in range(3, 11):
            stream += bytes([0xFF, 0xFF, page_num]) + bytes([page_num] * 16384)
        with tempfile.NamedTemporaryFile(suffix='.z80', delete=False) as f:
            f.write(stream)
            fn = f.name
        try:
            load_z80(fn, cpu)
            self.assertEqual(5, ram.page_select)
            # bank 0 was fed page_num 3 -> value 3
            self.assertEqual(3, ram.pages[0][0])
            self.assertEqual(10, ram.pages[7][0])
        finally:
            os.unlink(fn)


if __name__ == '__main__':
    unittest.main()
