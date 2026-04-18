# ZX Spectrum 128K banked memory
#
# Memory map:
#   0x0000-0x3FFF  one of two ROMs (editor ROM 0 or 48K BASIC ROM 1)
#   0x4000-0x7FFF  RAM page 5 (fixed; also the default screen)
#   0x8000-0xBFFF  RAM page 2 (fixed)
#   0xC000-0xFFFF  one of RAM pages 0..7 (paged)
#
# Paging is controlled by writes to port 0x7FFD:
#   bits 0..2  select the RAM page at 0xC000 (0..7)
#   bit  3     screen select (0 = page 5, 1 = shadow page 7)
#   bit  4     ROM select (0 = editor, 1 = 48K BASIC)
#   bit  5     paging lock — once set, further writes are ignored until reset


PAGE_SIZE = 0x4000
NUM_RAM_PAGES = 8
NUM_ROM_BANKS = 2


class BankedRAM:
    def __init__(self):
        self.rom_banks = [bytearray(PAGE_SIZE) for _ in range(NUM_ROM_BANKS)]
        self.pages = [bytearray(PAGE_SIZE) for _ in range(NUM_RAM_PAGES)]
        self.rom_select = 0
        self.page_select = 0
        self.screen_select = 0
        self.paging_locked = False

    def __getitem__(self, addr):
        addr &= 0xFFFF
        if addr < 0x4000:
            return self.rom_banks[self.rom_select][addr]
        if addr < 0x8000:
            return self.pages[5][addr - 0x4000]
        if addr < 0xC000:
            return self.pages[2][addr - 0x8000]
        return self.pages[self.page_select][addr - 0xC000]

    def __setitem__(self, addr, value):
        addr &= 0xFFFF
        value &= 0xFF
        if addr < 0x4000:
            return  # ROM — writes ignored
        if addr < 0x8000:
            self.pages[5][addr - 0x4000] = value
        elif addr < 0xC000:
            self.pages[2][addr - 0x8000] = value
        else:
            self.pages[self.page_select][addr - 0xC000] = value

    def write_port_7ffd(self, value):
        if self.paging_locked:
            return
        self.page_select = value & 0x07
        self.screen_select = (value >> 3) & 1
        self.rom_select = (value >> 4) & 1
        if value & 0x20:
            self.paging_locked = True

    def load_rom(self, bank, data):
        if bank not in (0, 1):
            raise ValueError("ROM bank must be 0 or 1")
        n = min(len(data), PAGE_SIZE)
        self.rom_banks[bank][:n] = data[:n]

    def load(self, rom):
        """No-op for duck-type compatibility with the 48K RAM class.
        On 128K, ROM lives in rom_banks — use load_rom(bank, data) instead."""
        return

    def clear(self):
        for p in self.pages:
            for i in range(PAGE_SIZE):
                p[i] = 0

    @property
    def current_screen(self):
        return self.pages[5 if self.screen_select == 0 else 7]
