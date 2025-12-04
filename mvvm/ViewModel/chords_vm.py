import threading
import queue
from dataclasses import dataclass
from typing import List, Dict

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 44100
CAPTURE_SECONDS = 2.0


@dataclass
class ChordDetectionResult:
    summary_text: str
    detail_text: str
    dominant_freqs: List[float]
    note_labels: List[str]
    magnitudes: List[float]


class ChordDetectorViewModel:
    def __init__(self) -> None:
        self.result_queue: "queue.Queue[ChordDetectionResult | str]" = queue.Queue()

        self._note_name_latin: Dict[str, str] = {
            "C": "Do",
            "C#": "Do#",
            "D": "Re",
            "D#": "Re#",
            "E": "Mi",
            "F": "Fa",
            "F#": "Fa#",
            "G": "Sol",
            "G#": "Sol#",
            "A": "La",
            "A#": "La#",
            "B": "Si",
        }

        self._note_reference_freq: Dict[str, float] = {
            "C": 261.63,
            "C#": 277.18,
            "D": 293.66,
            "D#": 311.13,
            "E": 329.63,
            "F": 349.23,
            "F#": 369.99,
            "G": 392.00,
            "G#": 415.30,
            "A": 440.00,
            "A#": 466.16,
            "B": 493.88,
        }

        self._chord_dictionary: Dict[str, set[str]] = self._build_chord_dictionary()

    def _build_chord_dictionary(self) -> Dict[str, set[str]]:
        chords: Dict[str, set[str]] = {}
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        for i, root in enumerate(notes):
            third_major = notes[(i + 4) % 12]
            fifth = notes[(i + 7) % 12]
            chords[root] = {root, third_major, fifth}

            third_minor = notes[(i + 3) % 12]
            chords[root + "m"] = {root, third_minor, fifth}

        return chords

    def _frequency_to_note_name(self, frequency: float) -> str:
        if frequency <= 0:
            return "N/A"

        n = 69 + 12 * np.log2(frequency / 440.0)
        midi_note = int(round(n))

        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        note_index = midi_note % 12
        octave = (midi_note // 12) - 1
        return f"{note_names[note_index]}{octave}"

    def _detect_dominant_frequencies(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        n_peaks: int = 5,
    ) -> tuple[list[float], list[float]]:
        window = np.hanning(len(audio_data))
        windowed = audio_data * window

        spectrum = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(windowed), d=1.0 / sample_rate)

        magnitudes = np.abs(spectrum)

        min_freq = 50.0
        valid_indices = np.where(freqs >= min_freq)[0]
        freqs = freqs[valid_indices]
        magnitudes = magnitudes[valid_indices]

        if len(freqs) == 0:
            return [], []

        if n_peaks >= len(magnitudes):
            peak_indices = np.argsort(magnitudes)[::-1]
        else:
            peak_indices = np.argpartition(magnitudes, -n_peaks)[-n_peaks:]
            peak_indices = peak_indices[np.argsort(magnitudes[peak_indices])[::-1]]

        dominant_freqs = freqs[peak_indices]
        dominant_mags = magnitudes[peak_indices]

        order = np.argsort(dominant_freqs)
        dominant_freqs = dominant_freqs[order]
        dominant_mags = dominant_mags[order]

        return dominant_freqs.tolist(), dominant_mags.tolist()

    def detect_chord_from_audio(self, audio_data: np.ndarray, sample_rate: int) -> ChordDetectionResult:
        if audio_data.ndim > 1:
            audio_data = np.mean(audio_data, axis=1)

        dominant_freqs, dominant_mags = self._detect_dominant_frequencies(audio_data, sample_rate)

        if not dominant_freqs:
            return ChordDetectionResult(
                summary_text="No se detectó señal suficiente",
                detail_text="",
                dominant_freqs=[],
                note_labels=[],
                magnitudes=[],
            )

        notes: List[str] = []
        note_labels_latin: List[str] = []
        for f in dominant_freqs:
            note_with_octave = self._frequency_to_note_name(f)
            if note_with_octave == "N/A":
                continue
            note_name = "".join([c for c in note_with_octave if not c.isdigit()])
            notes.append(note_name)
            latin = self._note_name_latin.get(note_name, note_name)
            note_labels_latin.append(latin)

        if not notes:
            return ChordDetectionResult(
                summary_text="No se pudieron mapear notas",
                detail_text="",
                dominant_freqs=[],
                note_labels=[],
                magnitudes=[],
            )

        note_set = set(notes)

        best_match = None
        best_score = 0

        for chord_name, chord_notes in self._chord_dictionary.items():
            intersection = len(chord_notes & note_set)
            if intersection > best_score:
                best_score = intersection
                best_match = chord_name

        if best_match is None or best_score == 0:
            return ChordDetectionResult(
                summary_text="Acorde no reconocido",
                detail_text="",
                dominant_freqs=dominant_freqs,
                note_labels=note_labels_latin,
                magnitudes=dominant_mags,
            )

        detected_notes_sorted = sorted(note_set)
        detected_notes_latin_sorted = [self._note_name_latin.get(n, n) for n in detected_notes_sorted]
        detected_notes_latin_str = ", ".join(detected_notes_latin_sorted)

        root_name = best_match.rstrip("m")
        quality = "menor" if best_match.endswith("m") else "mayor"
        root_latin = self._note_name_latin.get(root_name, root_name)
        summary_text = f"Acorde estimado: {root_latin} {quality} ({best_match})"

        freqs_str = ", ".join(f"{f:.2f} Hz" for f in dominant_freqs)

        chord_notes = self._chord_dictionary.get(best_match, set())
        theoretical_parts: List[str] = []
        for n in sorted(chord_notes):
            ref_freq = self._note_reference_freq.get(n)
            latin = self._note_name_latin.get(n, n)
            if ref_freq is not None:
                theoretical_parts.append(f"{latin} ≈ {ref_freq:.2f} Hz")
            else:
                theoretical_parts.append(f"{latin}")
        theoretical_str = ", ".join(theoretical_parts) if theoretical_parts else "(sin referencia)"

        detail_lines = [
            f"Frecuencias dominantes detectadas: {freqs_str}",
            f"Frecuencias teóricas aproximadas de las notas del acorde: {theoretical_str}",
        ]

        return ChordDetectionResult(
            summary_text=summary_text,
            detail_text="\n".join(detail_lines),
            dominant_freqs=dominant_freqs,
            note_labels=note_labels_latin,
            magnitudes=dominant_mags,
        )

    def analyze_once_async(self) -> None:
        def worker() -> None:
            try:
                num_samples = int(CAPTURE_SECONDS * SAMPLE_RATE)
                audio = sd.rec(
                    frames=num_samples,
                    samplerate=SAMPLE_RATE,
                    channels=1,
                    dtype="float32",
                )
                sd.wait()

                result = self.detect_chord_from_audio(audio.flatten(), SAMPLE_RATE)
                self.result_queue.put(result)
            except Exception as e:  # noqa: BLE001
                self.result_queue.put(f"Error grabando/detectando: {e}")

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
