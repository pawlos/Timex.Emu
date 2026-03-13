import tests_suite

import os
import tempfile
import unittest
from ram import RAM


class tests_ram(unittest.TestCase):

    def test_loadProgramAt_preserves_ram_size(self):
        ram = RAM()
        # Create a temp file with 4 bytes of data
        # but a filename longer than 4 chars
        with tempfile.NamedTemporaryFile(
            prefix='test_program_longname_',
            suffix='.bin',
            delete=False
        ) as f:
            f.write(b'\x01\x02\x03\x04')
            fname = f.name

        try:
            ram.loadProgramAt(fname, 0x8000)
            # RAM should still be 65536 bytes
            self.assertEqual(65536, len(ram.ram))
            # The 4 bytes should be loaded at 0x8000
            self.assertEqual(0x01, ram[0x8000])
            self.assertEqual(0x02, ram[0x8001])
            self.assertEqual(0x03, ram[0x8002])
            self.assertEqual(0x04, ram[0x8003])
            # Byte after the program should be 0 (untouched)
            self.assertEqual(0x00, ram[0x8004])
        finally:
            os.unlink(fname)
