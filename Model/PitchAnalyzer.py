import math
import librosa

class PitchAnalyzer:
    def __init__(self):
        self.NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.A4 = 440.0
        self.A4_MIDI = 69

    def freq_to_note(self, freq):
        if freq < 80 or freq > 1318:
            return None, 0
        midi = 12 * math.log2(freq / self.A4) + self.A4_MIDI
        midi_r = round(midi)
        if midi_r < 28 or midi_r > 88:
            return None, 0
        note = self.NOTE_NAMES[midi_r % 12]
        octave = midi_r // 12 - 1
        expected = self.A4 * (2 ** ((midi_r - self.A4_MIDI) / 12))
        cents = 1200 * math.log2(freq / expected) if expected > 0 else 0
        return f"{note}{octave}", round(cents)