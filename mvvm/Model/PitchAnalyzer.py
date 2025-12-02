import math

class PitchAnalyzer:
    # Afinación estándar (frecuencias exactas de cuerdas al aire)
    OPEN_STRINGS = [82.41, 110.00, 146.83, 196.00,
                    246.94, 329.63]  # E2 A2 D3 G3 B3 E4
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    A4 = 440.0

    def freq_to_note(self, freq):
        if freq is None or freq < 40 or freq > 1318:
            return None, 0, [], 0
        midi = 69 + 12 * math.log2(freq / self.A4)
        note_num = round(midi) % 12
        octave = int(round(midi)) // 12 - 1
        note_name = self.NOTES[note_num] + str(octave)
        cents = int(
            1200 * math.log2(freq / (self.A4 * 2**((round(midi)-69)/12))))

        # Buscar todas las posiciones de la nota en el diapasón (6 cuerdas, 0-19 trastes)
        positions = []
        for string, base in enumerate(self.OPEN_STRINGS, 1):
            for fret in range(0, 20):
                note_freq = base * (2 ** (fret / 12.0))
                midi_fret = 69 + 12 * math.log2(note_freq / self.A4)
                note_num_fret = round(midi_fret) % 12
                octave_fret = int(round(midi_fret)) // 12 - 1
                note_name_fret = self.NOTES[note_num_fret] + str(octave_fret)
                if note_name_fret == note_name:
                    positions.append((string, fret))

        return note_name, cents, positions, freq
