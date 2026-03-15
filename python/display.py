# ZX Spectrum / Timex 2048 Display Emulation
import pygame
import array

# Screen constants
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192
BORDER_SIZE = 32
SCALE = 2

# Memory addresses
BITMAP_START = 0x4000
ATTR_START = 0x5800

# ZX Spectrum colors (R, G, B)
COLORS = [
    # Normal
    (0, 0, 0),        # 0: black
    (0, 0, 205),      # 1: blue
    (205, 0, 0),      # 2: red
    (205, 0, 205),    # 3: magenta
    (0, 205, 0),      # 4: green
    (0, 205, 205),    # 5: cyan
    (205, 205, 0),    # 6: yellow
    (205, 205, 205),  # 7: white
    # Bright
    (0, 0, 0),        # 8: black (bright)
    (0, 0, 255),      # 9: blue (bright)
    (255, 0, 0),      # 10: red (bright)
    (255, 0, 255),    # 11: magenta (bright)
    (0, 255, 0),      # 12: green (bright)
    (0, 255, 255),    # 13: cyan (bright)
    (255, 255, 0),    # 14: yellow (bright)
    (255, 255, 255),  # 15: white (bright)
]

# ZX Spectrum keyboard matrix
# Each half-row is 5 keys, active low (0 = pressed)
# Index by half-row number (0-7)
# Row 0 (0xFE): SHIFT, Z, X, C, V
# Row 1 (0xFD): A, S, D, F, G
# Row 2 (0xFB): Q, W, E, R, T
# Row 3 (0xF7): 1, 2, 3, 4, 5
# Row 4 (0xEF): 0, 9, 8, 7, 6
# Row 5 (0xDF): P, O, I, U, Y
# Row 6 (0xBF): ENTER, L, K, J, H
# Row 7 (0x7F): SPACE, SYM_SHIFT, M, N, B

# Map pygame key -> (row, bit)
KEY_MAP = {
    # Row 0 (0xFE)
    pygame.K_LSHIFT: (0, 0), pygame.K_RSHIFT: (0, 0),
    pygame.K_z: (0, 1), pygame.K_x: (0, 2),
    pygame.K_c: (0, 3), pygame.K_v: (0, 4),
    # Row 1 (0xFD)
    pygame.K_a: (1, 0), pygame.K_s: (1, 1),
    pygame.K_d: (1, 2), pygame.K_f: (1, 3), pygame.K_g: (1, 4),
    # Row 2 (0xFB)
    pygame.K_q: (2, 0), pygame.K_w: (2, 1),
    pygame.K_e: (2, 2), pygame.K_r: (2, 3), pygame.K_t: (2, 4),
    # Row 3 (0xF7)
    pygame.K_1: (3, 0), pygame.K_2: (3, 1),
    pygame.K_3: (3, 2), pygame.K_4: (3, 3), pygame.K_5: (3, 4),
    # Row 4 (0xEF)
    pygame.K_0: (4, 0), pygame.K_9: (4, 1),
    pygame.K_8: (4, 2), pygame.K_7: (4, 3), pygame.K_6: (4, 4),
    # Row 5 (0xDF)
    pygame.K_p: (5, 0), pygame.K_o: (5, 1),
    pygame.K_i: (5, 2), pygame.K_u: (5, 3), pygame.K_y: (5, 4),
    # Row 6 (0xBF)
    pygame.K_RETURN: (6, 0), pygame.K_l: (6, 1),
    pygame.K_k: (6, 2), pygame.K_j: (6, 3), pygame.K_h: (6, 4),
    # Row 7 (0x7F)
    pygame.K_SPACE: (7, 0), pygame.K_LCTRL: (7, 1), pygame.K_RCTRL: (7, 1),
    pygame.K_m: (7, 2), pygame.K_n: (7, 3), pygame.K_b: (7, 4),
}


# Audio constants
SAMPLE_RATE = 44100
SAMPLES_PER_FRAME = SAMPLE_RATE // 50  # 882 samples per 20ms frame
SPEAKER_VOLUME = 8000  # 16-bit signed amplitude


class Display:
    def __init__(self, scale=SCALE):
        pygame.init()
        self.audio_enabled = False
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)
            self.audio_enabled = True
        except Exception:
            print("[!] Audio init failed, running without sound")
        self.scale = scale
        total_w = (SCREEN_WIDTH + BORDER_SIZE * 2) * scale
        total_h = (SCREEN_HEIGHT + BORDER_SIZE * 2) * scale
        self.screen = pygame.display.set_mode((total_w, total_h))
        pygame.display.set_caption("Timex 2048")
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.border_color = COLORS[7]
        self.frame_count = 0
        self.flash_state = False
        # Keyboard state: 8 half-rows, all keys released (0xFF = no keys pressed)
        self.key_rows = [0xFF] * 8
        # Speaker state for beeper audio
        self.speaker_state = 0
        self.speaker_toggles = []  # list of (tstates, state) pairs per frame
        self.frame_tstates = 0  # current T-state counter within frame

    def set_border(self, color_index):
        self.border_color = COLORS[color_index & 7]

    def set_speaker(self, state, tstates):
        self.speaker_state = state
        self.speaker_toggles.append((tstates, state))

    def _render_audio(self):
        if not self.audio_enabled or not self.speaker_toggles:
            return
        samples = array.array('h')  # signed 16-bit
        toggles = self.speaker_toggles
        tstates_per_sample = 69888 / SAMPLES_PER_FRAME
        toggle_idx = 0
        current_state = toggles[0][1] if toggles else 0
        for i in range(SAMPLES_PER_FRAME):
            sample_tstate = i * tstates_per_sample
            while toggle_idx < len(toggles) and toggles[toggle_idx][0] <= sample_tstate:
                current_state = toggles[toggle_idx][1]
                toggle_idx += 1
            samples.append(SPEAKER_VOLUME if current_state else -SPEAKER_VOLUME)
        self.speaker_toggles = []
        sound = pygame.mixer.Sound(buffer=samples)
        sound.play()


    def read_keyboard(self, high_byte):
        result = 0xFF
        for row in range(8):
            if not (high_byte & (1 << row)):
                result &= self.key_rows[row]
        return result

    def render(self, ram):
        self.frame_count += 1
        if self.frame_count % 16 == 0:
            self.flash_state = not self.flash_state

        set_at = self.surface.set_at

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

                if (attr & 0x80) and self.flash_state:
                    ink, paper = paper, ink

                x = col * 8
                for bit in range(8):
                    if byte & (0x80 >> bit):
                        set_at((x + bit, y), ink)
                    else:
                        set_at((x + bit, y), paper)

        self.screen.fill(self.border_color)
        scaled = pygame.transform.scale(
            self.surface,
            (SCREEN_WIDTH * self.scale, SCREEN_HEIGHT * self.scale))
        self.screen.blit(scaled, (BORDER_SIZE * self.scale, BORDER_SIZE * self.scale))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    filename = "screenshot_{}.png".format(self.frame_count)
                    pygame.image.save(self.screen, filename)
                    print("[+] Screenshot saved: {}".format(filename))
                    continue
                mapping = KEY_MAP.get(event.key)
                if mapping:
                    row, bit = mapping
                    self.key_rows[row] &= ~(1 << bit)
            elif event.type == pygame.KEYUP:
                mapping = KEY_MAP.get(event.key)
                if mapping:
                    row, bit = mapping
                    self.key_rows[row] |= (1 << bit)

    def update(self, ram):
        self.handle_events()
        self.render(ram)
        self._render_audio()

    def close(self):
        pygame.quit()
