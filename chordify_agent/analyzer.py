"""
MIDI chord analyzer with intelligent recognition.

Uses music21 for advanced chord analysis with custom heuristic fallbacks
for robust chord name detection.
"""

from typing import List, Tuple, Dict, Any, Optional


class ChordAnalyzer:
    """Analyze MIDI notes and convert to chord names."""

    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, use_music21: bool = True):
        """
        Initialize chord analyzer.

        Args:
            use_music21: Whether to use music21 for advanced recognition.
                        Falls back to heuristics if unavailable.
        """
        self.use_music21 = use_music21
        self._music21_available = False

        if use_music21:
            try:
                from music21 import chord as m21chord
                from music21.harmony import chordSymbolFigureFromChord

                self._m21chord = m21chord
                self._chordSymbolFigureFromChord = chordSymbolFigureFromChord
                self._music21_available = True
            except ImportError:
                pass

    def midi_to_note_names(self, midi_notes: List[int]) -> List[str]:
        """
        Convert MIDI note numbers to readable note names with octaves.

        Args:
            midi_notes: List of MIDI note numbers (0-127)

        Returns:
            List of note names with octaves (e.g. ["C4", "E4", "G4"])
        """
        if not midi_notes:
            return []

        result = []
        for midi_note in sorted(midi_notes):
            octave = (midi_note // 12) - 1  # MIDI octave calculation
            note_name = self.NOTE_NAMES[midi_note % 12]
            result.append(f"{note_name}{octave}")

        return result

    def analyze_chord(
        self, midi_notes: List[int], confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Analyze a chord from MIDI note numbers.

        Args:
            midi_notes: List of MIDI note numbers
            confidence_threshold: Minimum confidence for chord recognition (0.0-1.0)

        Returns:
            Dictionary with chord analysis:
            {
                "chord_name": str,      # e.g. "Cmaj7"
                "notes": List[str],     # e.g. ["C4", "E4", "G4", "B4"]
                "midi_notes": List[int],# Original MIDI numbers
                "note_count": int,      # Number of unique notes
                "confidence": float,    # Recognition confidence
                "method": str           # "music21" or "heuristic"
            }
        """
        if not midi_notes:
            return {
                "chord_name": "Rest",
                "notes": [],
                "midi_notes": [],
                "note_count": 0,
                "confidence": 1.0,
                "method": "builtin",
            }

        # Try music21 first
        if self._music21_available:
            try:
                m21_chord = self._m21chord.Chord(midi_notes)
                symbol = self._chordSymbolFigureFromChord(m21_chord)
                if symbol:
                    # Normalize power chord notation (Cpower → C5)
                    if symbol.endswith("power"):
                        symbol = symbol.replace("power", "5")
                    
                    return {
                        "chord_name": symbol,
                        "notes": self.midi_to_note_names(midi_notes),
                        "midi_notes": sorted(midi_notes),
                        "note_count": len(midi_notes),
                        "confidence": 0.95,
                        "method": "music21",
                    }
            except Exception:
                # Fall through to heuristic method
                pass

        # Heuristic fallback
        chord_name = self._heuristic_chord_name(midi_notes)
        confidence = self._estimate_confidence(midi_notes, chord_name)

        return {
            "chord_name": chord_name,
            "notes": self.midi_to_note_names(midi_notes),
            "midi_notes": sorted(midi_notes),
            "note_count": len(midi_notes),
            "confidence": confidence,
            "method": "heuristic",
        }

    def _heuristic_chord_name(self, midi_notes: List[int]) -> str:
        """
        Apply heuristic chord recognition when music21 unavailable.

        Recognizes common chord types: major, minor, diminished, augmented,
        sevenths, ninths, and various extensions.
        """
        notes = sorted(list(set(midi_notes)))

        if len(notes) == 1:
            root_note = notes[0] % 12
            return self.NOTE_NAMES[root_note]

        # Get root (lowest note)
        root_note = notes[0] % 12
        root_name = self.NOTE_NAMES[root_note]

        if len(notes) == 2:
            interval = (notes[1] - notes[0]) % 12
            if interval == 7:
                return f"{root_name}5"  # Power chord
            else:
                return f"{root_name}2"  # Generic dyad

        # Analyze intervals from root
        intervals = sorted(list(set([(note - notes[0]) % 12 for note in notes[1:]])))

        # Interval detection
        has_maj3 = 4 in intervals
        has_min3 = 3 in intervals
        has_p5 = 7 in intervals
        has_dim5 = 6 in intervals
        has_aug5 = 8 in intervals
        has_min7 = 10 in intervals
        has_maj7 = 11 in intervals
        has_9 = 2 in intervals
        has_11 = 5 in intervals
        has_13 = 9 in intervals

        # Build chord name
        chord_name = root_name

        # Determine basic quality
        if has_min3 and has_dim5:
            chord_name += "dim"
        elif has_min3:
            chord_name += "m"
        elif has_maj3 and has_aug5:
            chord_name += "aug"
        elif has_maj3 and has_p5:
            pass  # Major, no modifier
        elif has_maj3 and has_dim5:
            chord_name += "7"  # Dominant with tritone
        elif not has_maj3 and not has_min3:
            # Sus chords
            if has_11:
                chord_name += "sus4"
            elif has_9:
                chord_name += "sus2"

        # Add 7th extensions
        if has_maj7:
            if "m" in chord_name:
                chord_name += "maj7"
            else:
                chord_name += "maj7"
        elif has_min7:
            chord_name += "7"

        # Add upper extensions
        extensions = []
        if has_13:
            extensions.append("13")
        elif has_11:
            extensions.append("11")
        elif has_9:
            extensions.append("9")

        if extensions:
            if chord_name.endswith("7") and not chord_name.endswith("maj7"):
                chord_name = chord_name[:-1]
            chord_name += extensions[0]

        # Handle very complex chords
        if len(intervals) > 5:
            return f"{chord_name}({len(notes)})"

        return chord_name

    def _estimate_confidence(self, midi_notes: List[int], chord_name: str) -> float:
        """
        Estimate confidence in chord recognition.

        Uses heuristics like note count, recognized intervals, and chord complexity.
        """
        note_count = len(set(midi_notes))

        # Simple chords = higher confidence
        if note_count <= 3:
            return 0.85
        elif note_count == 4:
            return 0.80
        elif note_count <= 6:
            return 0.70
        else:
            return 0.60


# Convenience functions
def midi_to_chord_name(midi_notes: List[int], use_music21: bool = True) -> str:
    """
    Quick conversion of MIDI notes to chord name.

    Args:
        midi_notes: List of MIDI note numbers
        use_music21: Use music21 for advanced recognition

    Returns:
        Chord name string (e.g. "Cmaj7")
    """
    analyzer = ChordAnalyzer(use_music21=use_music21)
    result = analyzer.analyze_chord(midi_notes)
    return result["chord_name"]


def analyze_chord(midi_notes: List[int]) -> Dict[str, Any]:
    """
    Analyze chord with full details.

    Args:
        midi_notes: List of MIDI note numbers

    Returns:
        Full chord analysis dictionary
    """
    analyzer = ChordAnalyzer(use_music21=True)
    return analyzer.analyze_chord(midi_notes)
