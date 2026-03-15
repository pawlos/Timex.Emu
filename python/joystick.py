# Kempston Joystick Emulation
# Port 0x1F: bit0=right, bit1=left, bit2=down, bit3=up, bit4=fire
import pygame

KEMPSTON_MAP = {
    pygame.K_RIGHT: 0x01,
    pygame.K_LEFT:  0x02,
    pygame.K_DOWN:  0x04,
    pygame.K_UP:    0x08,
    pygame.K_RALT:  0x10,
}


class Joystick:
    def __init__(self):
        self.state = 0x00

    def read(self, high_byte=0):
        return self.state

    def key_down(self, key):
        bit = KEMPSTON_MAP.get(key)
        if bit:
            self.state |= bit

    def key_up(self, key):
        bit = KEMPSTON_MAP.get(key)
        if bit:
            self.state &= ~bit
