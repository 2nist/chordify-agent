# chordify-agent

MIDI chord recognition and analysis with intelligent fallbacks.

Extracted from [python-midi-toolkit](https://github.com/2nist/python-midi-toolkit) to provide standalone chord analysis capabilities for music applications.

## Features

- **Intelligent Chord Recognition**: Uses music21 when available, falls back to custom heuristics
- **Comprehensive Chord Types**: Major, minor, diminished, augmented, sevenths, ninths, elevenths, thirteenths
- **Progression Analysis**: Detect patterns, complexity scoring, and common progressions
- **High Confidence**: Estimates recognition confidence for each chord
- **Zero Configuration**: Works out of the box with automatic fallbacks

## Installation

```bash
pip install chordify-agent
```

### Dependencies

- `mido` - MIDI file processing
- `music21` - Advanced music theory analysis (optional, highly recommended)

## Quick Start

### Analyze a Single Chord

```python
from chordify_agent import analyze_chord

# C major triad (MIDI notes: C, E, G)
result = analyze_chord([60, 64, 67])

print(result["chord_name"])    # "C" or "Cmaj"
print(result["notes"])          # ["C4", "E4", "G4"]
print(result["confidence"])     # 0.95 (high confidence)
```

### Analyze a Chord Progression

```python
from chordify_agent import analyze_progression

# I-IV-V-I progression in C major
progression = [
    [60, 64, 67],  # C
    [65, 69, 72],  # F
    [67, 71, 74],  # G
    [60, 64, 67],  # C
]

result = analyze_progression(progression)
print(result["chord_names"])        # ["C", "F", "G", "C"]
print(result["complexity_score"])   # 5/10
print(result["patterns"])            # ["Returns to root", ...]
```

## API Reference

### ChordAnalyzer

Main class for chord analysis.

```python
from chordify_agent import ChordAnalyzer

analyzer = ChordAnalyzer(use_music21=True)

# Analyze chord
result = analyzer.analyze_chord([60, 64, 67])
```

#### Methods

- `analyze_chord(midi_notes, confidence_threshold=0.7)` - Full chord analysis
- `midi_to_note_names(midi_notes)` - Convert MIDI numbers to note names (e.g., ["C4", "E4", "G4"])

#### Return Value

```python
{
    "chord_name": str,      # "Cmaj7", "Dm", "G7", etc.
    "notes": List[str],     # ["C4", "E4", "G4", "B4"]
    "midi_notes": List[int],# [60, 64, 67, 71]
    "note_count": int,      # Number of notes
    "confidence": float,    # 0.0-1.0 recognition confidence
    "method": str           # "music21" or "heuristic"
}
```

### ChordProgression

Analyze sequences of chords for patterns and complexity.

```python
from chordify_agent import ChordProgression

progression = ChordProgression()
result = progression.analyze_progression([[60, 64, 67], [65, 69, 72]])
```

#### Return Value

```python
{
    "chord_count": int,
    "unique_chords": int,
    "chord_names": List[str],
    "complexity_score": int,           # 0-10
    "average_notes_per_chord": float,
    "patterns": List[str],              # Detected patterns
    "chord_details": List[Dict]         # Full analysis for each chord
}
```

### Convenience Functions

```python
from chordify_agent import midi_to_chord_name, analyze_chord

# Quick chord name lookup
name = midi_to_chord_name([60, 64, 67])  # "C"

# Full analysis
details = analyze_chord([60, 64, 67, 71])  # Cmaj7
```

## Recognized Chord Types

- **Triads**: Major, minor, diminished, augmented
- **Power Chords**: Root + fifth (e.g., C5)
- **Suspended**: sus2, sus4
- **Sevenths**: Major 7th, dominant 7th, minor 7th
- **Extensions**: 9th, 11th, 13th chords
- **Complex**: Multi-note voicings and jazz chords

## Pattern Detection

The progression analyzer detects:

- ✅ Returns to root
- ✅ Contains minor chords
- ✅ Contains seventh chords
- ✅ Extended chords (9th, 11th, 13th)
- ✅ Diminished/augmented chords
- ✅ Suspended chords
- ✅ Common progressions (I-IV-V, etc.)

## Use Cases

- **MIDI Analysis**: Extract chord progressions from MIDI files
- **Music Theory Tools**: Chord recognition for educational software
- **DAW Integration**: Real-time chord display in digital audio workstations
- **Composition Tools**: Analyze and suggest chord progressions
- **Max for Live**: Integration with PowerTrioArranger and similar systems

## Integration with PowerTrioArranger

This module was extracted from PT4EGMDM4L and PowerTrioArranger to provide reusable chord analysis:

```javascript
// In Max/MSP Node.js scripts
const { execSync } = require('child_process');

const midiNotes = [60, 64, 67];
const cmd = `python -c "from chordify_agent import midi_to_chord_name; print(midi_to_chord_name(${JSON.stringify(midiNotes)}))"`;
const chordName = execSync(cmd).toString().trim();
// chordName = "C"
```

## Related Projects

- [python-midi-toolkit](https://github.com/2nist/python-midi-toolkit) - Original toolkit with dataset browser
- [PowerTrioArranger](https://github.com/2nist/PowerTrioArranger) - Max for Live composition system
- [PT4EGMDM4L](https://github.com/2nist/PT4EGMDM4L) - Companion Max system

## License

MIT
