"""Example usage of chordify-agent."""

from chordify_agent import ChordAnalyzer, ChordProgression, analyze_chord

# Initialize analyzer
analyzer = ChordAnalyzer(use_music21=True)

print("🎵 chordify-agent Examples\n")
print("=" * 50)

# Example 1: Analyze a single chord
print("\n1️⃣  Analyze C Major Triad")
print("-" * 50)
c_major = [60, 64, 67]  # C, E, G
result = analyzer.analyze_chord(c_major)
print(f"Chord name: {result['chord_name']}")
print(f"Notes: {result['notes']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Method: {result['method']}")

# Example 2: Analyze G7 chord
print("\n2️⃣  Analyze G7 (Dominant Seventh)")
print("-" * 50)
g7 = [67, 71, 74, 77]  # G, B, D, F
result = analyzer.analyze_chord(g7)
print(f"Chord name: {result['chord_name']}")
print(f"Notes: {result['notes']}")
print(f"Note count: {result['note_count']}")

# Example 3: Analyze a progression
print("\n3️⃣  Analyze Chord Progression (I-IV-V-I in C)")
print("-" * 50)
progression_analyzer = ChordProgression(analyzer)

progression = [
    [60, 64, 67],  # C major
    [65, 69, 72],  # F major
    [67, 71, 74],  # G major
    [60, 64, 67],  # C major
]

prog_result = progression_analyzer.analyze_progression(progression)
print(f"Chord sequence: {' → '.join(prog_result['chord_names'])}")
print(f"Unique chords: {prog_result['unique_chords']}")
print(f"Complexity: {prog_result['complexity_score']}/10")
print(f"Patterns detected:")
for pattern in prog_result["patterns"]:
    print(f"  • {pattern}")

# Example 4: Jazz progression with extensions
print("\n4️⃣  Analyze Jazz Progression")
print("-" * 50)
jazz_progression = [
    [60, 64, 67, 71],  # Cmaj7
    [69, 72, 76, 79],  # Am7
    [74, 77, 81, 84],  # Dm7
    [67, 71, 74, 77],  # G7
]

jazz_result = progression_analyzer.analyze_progression(jazz_progression)
print(f"Chord sequence: {' → '.join(jazz_result['chord_names'])}")
print(f"Average notes/chord: {jazz_result['average_notes_per_chord']}")
print(f"Complexity: {jazz_result['complexity_score']}/10")
print(f"Patterns:")
for pattern in jazz_result["patterns"]:
    print(f"  • {pattern}")

# Example 5: Quick convenience function
print("\n5️⃣  Quick Chord Identification")
print("-" * 50)
from chordify_agent import midi_to_chord_name

quick_chords = [
    [60, 63, 67],  # C minor
    [62, 66, 69],  # D major
    [64, 68, 71],  # E major
]

for midi_notes in quick_chords:
    name = midi_to_chord_name(midi_notes)
    notes = analyzer.midi_to_note_names(midi_notes)
    print(f"{name:8s} → {', '.join(notes)}")

print("\n" + "=" * 50)
print("✅ Examples complete!\n")
