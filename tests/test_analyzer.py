"""Test chord analyzer functionality."""

from chordify_agent import ChordAnalyzer, midi_to_chord_name, analyze_chord


def test_major_triad():
    """Test C major chord recognition."""
    # C major: C-E-G (MIDI: 60, 64, 67)
    result = analyze_chord([60, 64, 67])
    print(f"✓ C major: {result['chord_name']}")
    assert result["chord_name"] in ["C", "Cmaj"],  f"Expected C/Cmaj, got {result['chord_name']}"
    assert result["note_count"] == 3


def test_minor_triad():
    """Test A minor chord recognition."""
    # A minor: A-C-E (MIDI: 69, 72, 76)
    result = analyze_chord([69, 72, 76])
    print(f"✓ A minor: {result['chord_name']}")
    assert "m" in result["chord_name"] or result["chord_name"] == "Am"
    assert result["note_count"] == 3


def test_seventh_chord():
    """Test G7 chord recognition."""
    # G7: G-B-D-F (MIDI: 67, 71, 74, 77)
    result = analyze_chord([67, 71, 74, 77])
    print(f"✓ G7: {result['chord_name']}")
    assert "7" in result["chord_name"]
    assert result["note_count"] == 4


def test_power_chord():
    """Test power chord (root + fifth)."""
    # C5: C-G (MIDI: 60, 67)
    result = analyze_chord([60, 67])
    print(f"✓ C5 (power): {result['chord_name']}")
    assert result["chord_name"] in ["C5", "C2"]
    assert result["note_count"] == 2


def test_diminished():
    """Test diminished chord."""
    # Bdim: B-D-F (MIDI: 71, 74, 77)
    result = analyze_chord([71, 74, 77])
    print(f"✓ B diminished: {result['chord_name']}")
    assert result["note_count"] == 3


def test_rest():
    """Test empty chord (rest)."""
    result = analyze_chord([])
    print(f"✓ Rest: {result['chord_name']}")
    assert result["chord_name"] == "Rest"
    assert result["note_count"] == 0
    assert result["confidence"] == 1.0


def test_note_names():
    """Test MIDI to note name conversion."""
    analyzer = ChordAnalyzer()
    notes = analyzer.midi_to_note_names([60, 64, 67])
    print(f"✓ Note names: {notes}")
    assert notes == ["C4", "E4", "G4"]


def test_quick_functions():
    """Test convenience functions."""
    name = midi_to_chord_name([60, 64, 67])
    print(f"✓ Quick conversion: {name}")
    assert name in ["C", "Cmaj"]


if __name__ == "__main__":
    print("\n🧪 Testing chordify-agent chord analyzer...\n")

    test_major_triad()
    test_minor_triad()
    test_seventh_chord()
    test_power_chord()
    test_diminished()
    test_rest()
    test_note_names()
    test_quick_functions()

    print("\n✅ All tests passed!\n")
