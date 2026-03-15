# ZX Spectrum Beeper Sound Emulation
import platform
import pygame
import array

SAMPLE_RATE = 44100
SAMPLES_PER_FRAME = SAMPLE_RATE // 50
SPEAKER_VOLUME = 8000

_is_pypy = platform.python_implementation() == 'PyPy'


class Beeper:
    def __init__(self):
        self.audio_enabled = False
        if not _is_pypy:
            try:
                pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)
                self.audio_enabled = True
            except Exception:
                print("[!] Audio init failed, running without sound")
        else:
            print("[!] PyPy detected, audio disabled")
        self.speaker_state = 0
        self.speaker_toggles = []

    def set_speaker(self, state, tstates):
        self.speaker_state = state
        self.speaker_toggles.append((tstates, state))

    def render_audio(self):
        if not self.audio_enabled or not self.speaker_toggles:
            return
        samples = array.array('h')
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
