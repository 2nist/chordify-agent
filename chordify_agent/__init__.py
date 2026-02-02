"""
chordify-agent: MIDI chord recognition and analysis

Provides intelligent chord name recognition from MIDI note collections
with music21 integration and custom heuristic fallbacks.
"""

from .analyzer import ChordAnalyzer, analyze_chord, midi_to_chord_name
from .progression import ChordProgression, analyze_progression

__version__ = "1.0.0"
__all__ = [
    "ChordAnalyzer",
    "analyze_chord",
    "midi_to_chord_name",
    "ChordProgression",
    "analyze_progression",
]
