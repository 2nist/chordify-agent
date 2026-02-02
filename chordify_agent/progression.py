"""
Chord progression analysis and pattern detection.
"""

from typing import List, Dict, Any, Tuple
from .analyzer import ChordAnalyzer


class ChordProgression:
    """Analyze sequences of chords for patterns and complexity."""

    def __init__(self, analyzer: ChordAnalyzer = None):
        """
        Initialize progression analyzer.

        Args:
            analyzer: ChordAnalyzer instance (creates new if None)
        """
        self.analyzer = analyzer or ChordAnalyzer(use_music21=True)

    def analyze_progression(
        self, midi_chord_sequence: List[List[int]]
    ) -> Dict[str, Any]:
        """
        Analyze a sequence of MIDI chord groups.

        Args:
            midi_chord_sequence: List of MIDI note lists, e.g.:
                [[60, 64, 67], [65, 69, 72], ...]  # C major, F major, ...

        Returns:
            Dictionary with progression analysis:
            {
                "chord_count": int,
                "unique_chords": int,
                "chord_names": List[str],
                "complexity_score": int (0-10),
                "average_notes_per_chord": float,
                "patterns": List[str],
                "chord_details": List[Dict]  # Full analysis for each chord
            }
        """
        if not midi_chord_sequence:
            return {
                "chord_count": 0,
                "unique_chords": 0,
                "chord_names": [],
                "complexity_score": 0,
                "average_notes_per_chord": 0.0,
                "patterns": [],
                "chord_details": [],
            }

        # Analyze each chord
        chord_details = []
        chord_names = []

        for midi_notes in midi_chord_sequence:
            analysis = self.analyzer.analyze_chord(midi_notes)
            chord_details.append(analysis)
            chord_names.append(analysis["chord_name"])

        # Calculate statistics
        note_counts = [detail["note_count"] for detail in chord_details]
        avg_notes = sum(note_counts) / len(note_counts) if note_counts else 0
        unique_chords = len(set(chord_names))

        # Complexity score (0-10)
        complexity_score = min(int(unique_chords * 1.5 + avg_notes), 10)

        # Detect patterns
        patterns = self._detect_patterns(chord_names)

        return {
            "chord_count": len(midi_chord_sequence),
            "unique_chords": unique_chords,
            "chord_names": chord_names,
            "complexity_score": complexity_score,
            "average_notes_per_chord": round(avg_notes, 1),
            "patterns": patterns,
            "chord_details": chord_details,
        }

    def _detect_patterns(self, chord_names: List[str]) -> List[str]:
        """
        Detect common patterns in chord progressions.

        Looks for:
        - Returns to root
        - Common progressions (I-IV-V, etc.)
        - Minor chord usage
        - Jazz patterns
        """
        patterns = []

        if len(chord_names) < 2:
            return patterns

        # Returns to root
        if chord_names[0] == chord_names[-1]:
            patterns.append("Returns to root")

        # Minor chords
        if any("m" in name and "maj" not in name for name in chord_names):
            patterns.append("Contains minor chords")

        # Seventh chords
        if any("7" in name for name in chord_names):
            patterns.append("Contains seventh chords")

        # Extensions (9th, 11th, 13th)
        if any(ext in name for name in chord_names for ext in ["9", "11", "13"]):
            patterns.append("Contains extended chords")

        # Diminished chords
        if any("dim" in name for name in chord_names):
            patterns.append("Contains diminished chords")

        # Augmented chords
        if any("aug" in name for name in chord_names):
            patterns.append("Contains augmented chords")

        # Suspended chords
        if any("sus" in name for name in chord_names):
            patterns.append("Contains suspended chords")

        # Common progressions (basic detection)
        chord_str = " ".join(chord_names[:4])
        if any(pattern in chord_str for pattern in ["C F G", "D G A"]):
            patterns.append("Contains I-IV-V pattern")

        return patterns


def analyze_progression(midi_chord_sequence: List[List[int]]) -> Dict[str, Any]:
    """
    Quick progression analysis.

    Args:
        midi_chord_sequence: List of MIDI note lists

    Returns:
        Full progression analysis dictionary
    """
    progression = ChordProgression()
    return progression.analyze_progression(midi_chord_sequence)
