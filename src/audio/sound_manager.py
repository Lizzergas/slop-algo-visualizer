import time
import numpy as np
import pygame
from typing import Optional, List, Dict
from src.state import AlgorithmState

class SoundManager:
    """Manages playing synthesized sounds for the sorting visualization using pygame."""
    
    def __init__(self, min_val: int, max_val: int, base_duration: float = 0.05):
        self.min_val = min_val
        self.max_val = max_val
        self.base_duration = max(0.01, base_duration)
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            
        # Pre-generate sounds to save CPU during rapid playback
        self.sounds: Dict[int, pygame.mixer.Sound] = {}
        self._pregenerate_sounds()

    def _map_value_to_frequency(self, value: int) -> float:
        """Map an array value to a frequency in Hz.
        Range is typically 150Hz (low pitch) to 1200Hz (high pitch).
        """
        min_freq = 150.0
        max_freq = 1200.0
        
        if self.max_val == self.min_val:
            return (min_freq + max_freq) / 2.0
            
        # Normalize between 0 and 1
        normalized = (value - self.min_val) / (self.max_val - self.min_val)
        
        # Exponential curve sounds better for pitch mapping than linear
        # frequency = min_freq * (max_freq / min_freq) ^ normalized
        freq = min_freq * ((max_freq / min_freq) ** normalized)
        return round(freq, 2)
        
    def _create_sine_wave(self, frequency: float) -> pygame.mixer.Sound:
        """Generate a sine wave sound object."""
        sample_rate = 44100
        t = np.linspace(0, self.base_duration, int(sample_rate * self.base_duration), False)
        
        # Apply a simple envelope (fade in/out) to prevent clicking
        envelope = np.ones_like(t)
        fade_len = int(sample_rate * 0.005) # 5ms fade
        if len(envelope) > fade_len * 2:
            envelope[:fade_len] = np.linspace(0, 1, fade_len)
            envelope[-fade_len:] = np.linspace(1, 0, fade_len)
            
        note = np.sin(frequency * t * 2 * np.pi) * envelope
        
        # Lower amplitude factor (13 instead of 14) to prevent speaker distortion
        audio = note * (2**13 - 1)
        audio = audio.astype(np.int16)
        sound = pygame.sndarray.make_sound(audio)
        sound.set_volume(0.15) # Halved default volume
        return sound

    def _pregenerate_sounds(self):
        """Pre-generate a sound for every possible value in our min/max range."""
        # Only pre-generate if the range isn't massive (e.g., > 2000 elements)
        if self.max_val - self.min_val < 2000:
            for val in range(self.min_val, self.max_val + 1):
                freq = self._map_value_to_frequency(val)
                self.sounds[val] = self._create_sine_wave(freq)

    def play_for_state(self, state: 'AlgorithmState') -> None:
        """Play a sound based on the current algorithm state."""
        # Decide which elements are active in this step
        active_indices = []
        if state.swapping:
            active_indices = state.swapping
        elif state.comparing:
            active_indices = state.comparing
            
        if not active_indices:
            return
            
        try:
            val = state.array[active_indices[0]]
            
            # Fetch pre-generated sound or generate on the fly
            if val in self.sounds:
                sound = self.sounds[val]
            else:
                freq = self._map_value_to_frequency(val)
                sound = self._create_sine_wave(freq)
                
            sound.play()
        except IndexError:
            pass

    def stop(self) -> None:
        """Terminate all currently playing sounds."""
        if pygame.mixer.get_init():
            pygame.mixer.stop()
