# ZX Spectrum Keyboard Emulation
import pygame

# Map pygame key -> (row, bit)
KEY_MAP = {
    # Row 0 (0xFE): SHIFT, Z, X, C, V
    pygame.K_LSHIFT: (0, 0), pygame.K_RSHIFT: (0, 0),
    pygame.K_z: (0, 1), pygame.K_x: (0, 2),
    pygame.K_c: (0, 3), pygame.K_v: (0, 4),
    # Row 1 (0xFD): A, S, D, F, G
    pygame.K_a: (1, 0), pygame.K_s: (1, 1),
    pygame.K_d: (1, 2), pygame.K_f: (1, 3), pygame.K_g: (1, 4),
    # Row 2 (0xFB): Q, W, E, R, T
    pygame.K_q: (2, 0), pygame.K_w: (2, 1),
    pygame.K_e: (2, 2), pygame.K_r: (2, 3), pygame.K_t: (2, 4),
    # Row 3 (0xF7): 1, 2, 3, 4, 5
    pygame.K_1: (3, 0), pygame.K_2: (3, 1),
    pygame.K_3: (3, 2), pygame.K_4: (3, 3), pygame.K_5: (3, 4),
    # Row 4 (0xEF): 0, 9, 8, 7, 6
    pygame.K_0: (4, 0), pygame.K_9: (4, 1),
    pygame.K_8: (4, 2), pygame.K_7: (4, 3), pygame.K_6: (4, 4),
    # Row 5 (0xDF): P, O, I, U, Y
    pygame.K_p: (5, 0), pygame.K_o: (5, 1),
    pygame.K_i: (5, 2), pygame.K_u: (5, 3), pygame.K_y: (5, 4),
    # Row 6 (0xBF): ENTER, L, K, J, H
    pygame.K_RETURN: (6, 0), pygame.K_l: (6, 1),
    pygame.K_k: (6, 2), pygame.K_j: (6, 3), pygame.K_h: (6, 4),
    # Row 7 (0x7F): SPACE, SYM_SHIFT, M, N, B
    pygame.K_SPACE: (7, 0), pygame.K_LCTRL: (7, 1), pygame.K_RCTRL: (7, 1),
    pygame.K_m: (7, 2), pygame.K_n: (7, 3), pygame.K_b: (7, 4),
}


class Keyboard:
    def __init__(self):
        self.key_rows = [0xFF] * 8

    def read(self, high_byte=0):
        result = 0xFF
        for row in range(8):
            if not (high_byte & (1 << row)):
                result &= self.key_rows[row]
        return result

    def key_down(self, key):
        mapping = KEY_MAP.get(key)
        if mapping:
            row, bit = mapping
            self.key_rows[row] &= ~(1 << bit)

    def key_up(self, key):
        mapping = KEY_MAP.get(key)
        if mapping:
            row, bit = mapping
            self.key_rows[row] |= (1 << bit)

    def handle_events(self, screen, joystick, machine=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    screen.screenshot()
                    continue
                if event.key == pygame.K_F1 and machine:
                    machine.paused = not machine.paused
                    state = "PAUSED" if machine.paused else "RESUMED"
                    print("[+] {}".format(state))
                    continue
                if event.key == pygame.K_F2 and machine:
                    machine.enter_debugger()
                    continue
                joystick.key_down(event.key)
                self.key_down(event.key)
            elif event.type == pygame.KEYUP:
                joystick.key_up(event.key)
                self.key_up(event.key)
