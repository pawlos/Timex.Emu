import tests_suite

import unittest
from banked_ram import BankedRAM


class tests_banked_ram(unittest.TestCase):

    def test_default_state(self):
        m = BankedRAM()
        # All RAM pages start zeroed
        for addr in (0x4000, 0x8000, 0xC000, 0xFFFF):
            self.assertEqual(0, m[addr])
        # Paging defaults: ROM 0, page 0 at 0xC000, screen page 5, unlocked
        self.assertEqual(0, m.rom_select)
        self.assertEqual(0, m.page_select)
        self.assertEqual(0, m.screen_select)
        self.assertFalse(m.paging_locked)

    def test_ram_writes_preserved(self):
        m = BankedRAM()
        m[0x4000] = 0x11
        m[0x8000] = 0x22
        m[0xC000] = 0x33
        m[0xFFFF] = 0x44
        self.assertEqual(0x11, m[0x4000])
        self.assertEqual(0x22, m[0x8000])
        self.assertEqual(0x33, m[0xC000])
        self.assertEqual(0x44, m[0xFFFF])

    def test_rom_writes_ignored(self):
        m = BankedRAM()
        m.load_rom(0, bytes([0xAA] * 0x4000))
        m[0x0000] = 0x55
        m[0x3FFF] = 0x55
        self.assertEqual(0xAA, m[0x0000])
        self.assertEqual(0xAA, m[0x3FFF])

    def test_rom_bank_switch(self):
        m = BankedRAM()
        m.load_rom(0, bytes([0xA0] * 0x4000))
        m.load_rom(1, bytes([0xB1] * 0x4000))
        self.assertEqual(0xA0, m[0x0100])  # ROM 0 active
        m.write_port_7ffd(0x10)             # bit 4 set -> ROM 1
        self.assertEqual(0xB1, m[0x0100])
        self.assertEqual(1, m.rom_select)

    def test_page_5_fixed_at_4000(self):
        # Page 5 is always visible at 0x4000-0x7FFF regardless of page_select.
        m = BankedRAM()
        m.pages[5][0x100] = 0x77
        self.assertEqual(0x77, m[0x4100])
        # Page in different RAM at 0xC000, page 5 at 0x4000 stays the same.
        m.write_port_7ffd(0x03)
        self.assertEqual(0x77, m[0x4100])

    def test_page_2_fixed_at_8000(self):
        m = BankedRAM()
        m.pages[2][0x200] = 0x88
        self.assertEqual(0x88, m[0x8200])
        m.write_port_7ffd(0x04)  # switch 0xC000 page, page 2 still at 0x8000
        self.assertEqual(0x88, m[0x8200])

    def test_paged_ram_at_c000(self):
        m = BankedRAM()
        # Write a distinct marker into every page at offset 0x10
        for i in range(8):
            m.pages[i][0x10] = 0xA0 + i
        # Each page select should expose its marker at 0xC010
        for i in range(8):
            m.write_port_7ffd(i)
            self.assertEqual(0xA0 + i, m[0xC010])

    def test_writes_to_c000_land_in_selected_page(self):
        m = BankedRAM()
        m.write_port_7ffd(0x03)
        m[0xC050] = 0xEE
        self.assertEqual(0xEE, m.pages[3][0x50])
        # Other pages untouched
        for i in range(8):
            if i == 3:
                continue
            self.assertEqual(0, m.pages[i][0x50])

    def test_screen_select_bit(self):
        m = BankedRAM()
        self.assertEqual(0, m.screen_select)
        m.write_port_7ffd(0x08)
        self.assertEqual(1, m.screen_select)
        m.write_port_7ffd(0x00)
        self.assertEqual(0, m.screen_select)

    def test_current_screen_returns_correct_page(self):
        m = BankedRAM()
        m.pages[5][0x100] = 0x55
        m.pages[7][0x100] = 0x77
        self.assertEqual(0x55, m.current_screen[0x100])
        m.write_port_7ffd(0x08)  # screen bit -> page 7
        self.assertEqual(0x77, m.current_screen[0x100])

    def test_paging_lock(self):
        m = BankedRAM()
        m.write_port_7ffd(0x20)   # set lock bit
        self.assertTrue(m.paging_locked)
        # Subsequent writes must be ignored
        m.write_port_7ffd(0x17)   # would select page 7, screen 1, ROM 1
        self.assertEqual(0, m.page_select)
        self.assertEqual(0, m.screen_select)
        self.assertEqual(0, m.rom_select)

    def test_clear_zeros_ram_but_not_rom(self):
        m = BankedRAM()
        m.load_rom(0, bytes([0xCC] * 0x4000))
        m[0xC000] = 0xFF
        m.pages[3][0x100] = 0xFF
        m.clear()
        self.assertEqual(0, m[0xC000])
        self.assertEqual(0, m.pages[3][0x100])
        self.assertEqual(0xCC, m[0x0000])  # ROM untouched

    def test_getitem_masks_addr_to_16_bits(self):
        m = BankedRAM()
        m[0x4000] = 0x99
        # 0x14000 wraps to 0x4000
        self.assertEqual(0x99, m[0x14000])


if __name__ == '__main__':
    unittest.main()
