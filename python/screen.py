# ZX Spectrum Screen Emulation
import pygame

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192
BORDER_SIZE = 32

BITMAP_START = 0x4000
ATTR_START = 0x5800

COLORS = [
    # Normal
    (0, 0, 0), (0, 0, 205), (205, 0, 0), (205, 0, 205),
    (0, 205, 0), (0, 205, 205), (205, 205, 0), (205, 205, 205),
    # Bright
    (0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 0, 255),
    (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 255, 255),
]


class Screen:
    def __init__(self, scale=2):
        pygame.init()
        self.scale = scale
        total_w = (SCREEN_WIDTH + BORDER_SIZE * 2) * scale
        total_h = (SCREEN_HEIGHT + BORDER_SIZE * 2) * scale
        self.window = pygame.display.set_mode((total_w, total_h))
        pygame.display.set_caption("Timex 2048")
        self.border_color = COLORS[7]
        self._pixel_buf = bytearray(SCREEN_WIDTH * SCREEN_HEIGHT * 3)
        self.frame_count = 0
        self.flash_state = False
        self.loading_stripes = None  # (color1, color2) when active

    def set_border(self, color_index):
        self.border_color = COLORS[color_index & 7]

    def _draw_striped_border(self):
        c1, c2 = self.loading_stripes
        win_w, win_h = self.window.get_size()
        stripe_h = self.scale * 8
        for y in range(0, win_h, stripe_h):
            color = c1 if (y // stripe_h) % 2 == 0 else c2
            self.window.fill(color, (0, y, win_w, stripe_h))

    def screenshot(self):
        filename = "screenshot_{}.png".format(self.frame_count)
        pygame.image.save(self.window, filename)
        print("[+] Screenshot saved: {}".format(filename))

    def render(self, ram):
        self.frame_count += 1
        if self.frame_count % 16 == 0:
            self.flash_state = not self.flash_state

        # Build pixel buffer in pure Python (3 bytes per pixel, RGB)
        buf = self._pixel_buf
        flash = self.flash_state
        idx = 0

        for y in range(SCREEN_HEIGHT):
            addr = (BITMAP_START
                    + ((y & 0xC0) << 5)
                    + ((y & 0x07) << 8)
                    + ((y & 0x38) << 2))
            attr_base = ATTR_START + (y >> 3) * 32

            for col in range(32):
                byte = ram[addr + col]
                attr = ram[attr_base + col]

                bright = 8 if attr & 0x40 else 0
                ink = COLORS[(attr & 0x07) + bright]
                paper = COLORS[((attr >> 3) & 0x07) + bright]

                if (attr & 0x80) and flash:
                    ink, paper = paper, ink

                for bit in range(8):
                    if byte & (0x80 >> bit):
                        r, g, b = ink
                    else:
                        r, g, b = paper
                    buf[idx] = r
                    buf[idx+1] = g
                    buf[idx+2] = b
                    idx += 3

        # One C call to create surface from buffer
        frame = pygame.image.frombuffer(buf, (SCREEN_WIDTH, SCREEN_HEIGHT), 'RGB')

        if self.loading_stripes:
            self._draw_striped_border()
        else:
            self.window.fill(self.border_color)
        scaled = pygame.transform.scale(
            frame,
            (SCREEN_WIDTH * self.scale, SCREEN_HEIGHT * self.scale))
        self.window.blit(scaled, (BORDER_SIZE * self.scale, BORDER_SIZE * self.scale))
        pygame.display.flip()

    def close(self):
        pygame.quit()
