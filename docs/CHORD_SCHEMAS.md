# Chord Progression Schema Reference

This document describes the JSON schema formats used for chord progression analysis, song structure representation, and dataset management in chordify-agent.

## 1. Chord Progression Schema

### Format Overview

```json
{
  "id": 1,
  "chords": ["C", "F", "G", "C"],
  "chord_count": 4,
  "complexity": 3,
  "patterns": ["Returns to root", "I-IV-V-I progression"]
}
```

### Field Definitions

| Field | Type | Range/Format | Description |
|-------|------|--------------|-------------|
| `id` | integer | > 0 | Unique progression identifier |
| `chords` | string[] | Valid chord symbols | Array of chord names in sequence |
| `chord_count` | integer | > 0 | Number of chords in progression |
| `complexity` | integer | 1-10 | Harmonic complexity score (see below) |
| `patterns` | string[] | Free text | Musical pattern descriptions/tags |

### Complexity Scoring

The `complexity` field rates harmonic sophistication on a 1-10 scale:

| Score | Description | Example Progressions |
|-------|-------------|---------------------|
| 1-3 | Simple diatonic | I-IV-V-I, I-V-vi-IV |
| 4-6 | Extended diatonic, common substitutions | vi-IV-I-V, I-vi-ii-V |
| 7-8 | Modal mixture, 7th chords, minor key | ii-V-I with extensions, modal interchange |
| 9-10 | Advanced harmony | Chromatic mediants, altered dominants, jazz voicings |

### Pattern Tags

Common `patterns` values include:

- **"Returns to root"** — Progression begins and ends on tonic
- **"I-IV-V-I progression"** — Classic Western harmony
- **"vi-IV-I-V progression"** — Pop/rock formula
- **"Circle of fifths"** — Root movement by descending fifths
- **"Contains minor chords"** — Mix of major/minor tonalities
- **"Contains 7th chord"** — Uses extended harmony (maj7, dom7, min7)
- **"Minor key center"** — Based in minor scale
- **"Extended progression"** — More than 6 unique chords

## 2. Song Structure Schema

### Format Overview

```json
{
  "title": "Test Song",
  "artist": "Test Artist",
  "key": "C",
  "tempo": 120,
  "time_signature": "4/4",
  "chord_progression": ["C", "F", "G", "C", "Am", "F", "C", "G"],
  "structure": {
    "verse": ["C", "F", "G", "C"],
    "chorus": ["Am", "F", "C", "G"],
    "bridge": ["F", "C", "G", "Am"]
  },
  "duration": 60
}
```

### Field Definitions

| Field | Type | Format | Required | Description |
|-------|------|--------|----------|-------------|
| `title` | string | - | Yes | Song title |
| `artist` | string | - | Yes | Artist/composer name |
| `key` | string | Note name (A-G) + accidental | Yes | Tonal center (e.g., "C", "F#m", "Bb") |
| `tempo` | integer | 40-240 BPM | Yes | Beats per minute |
| `time_signature` | string | "N/D" format | Yes | Meter (e.g., "4/4", "3/4", "6/8") |
| `chord_progression` | string[] | Valid chord symbols | Yes | Complete chord sequence |
| `structure` | object | Section → chords[] | Optional | Song form breakdown |
| `duration` | integer | Seconds | Optional | Total song length in seconds |

### Structure Object

The `structure` field maps section names to chord arrays:

```json
{
  "intro": ["C", "Am"],
  "verse": ["C", "F", "G", "C"],
  "prechorus": ["Am", "F", "G"],
  "chorus": ["Am", "F", "C", "G"],
  "bridge": ["Dm", "G", "C", "Am"],
  "outro": ["F", "G", "C"]
}
```

**Common section names:**
- `intro`, `verse`, `prechorus`, `chorus`, `bridge`, `interlude`, `solo`, `outro`

**Each section value** is a string array of chord symbols representing that section's harmonic content.

## 3. Dataset Browse Schema

### Request Format

```json
{
  "page": 1,
  "items_per_page": 10,
  "filter": {
    "min_complexity": 3,
    "max_complexity": 7,
    "min_length": 4,
    "max_length": 8,
    "required_patterns": ["Circle of fifths"]
  }
}
```

### Response Format

```json
{
  "progressions": [
    {
      "id": 1,
      "chords": ["C", "Am", "Dm", "G"],
      "chord_count": 4,
      "complexity": 5,
      "patterns": ["I-vi-ii-V progression", "Circle of fifths"]
    }
  ],
  "page": 1,
  "items_per_page": 10,
  "total_items": 1257279,
  "total_pages": 125728,
  "has_next": true,
  "has_previous": false
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `page` | integer | Current page number (1-indexed) |
| `items_per_page` | integer | Number of progressions per page (default: 10) |
| `total_items` | integer | Total progressions in dataset |
| `total_pages` | integer | Total pages available |
| `has_next` | boolean | True if page + 1 exists |
| `has_previous` | boolean | True if page > 1 |
| `progressions` | array | Array of progression objects (see schema 1) |

## 4. REAPER Export Schema (Lua)

### CHORD_INDEX Format

When exporting for REAPER integration, progressions are formatted as Lua tables:

```lua
CHORD_INDEX = {
  {
    id = 1,
    chords = {"C", "F", "G", "C"},
    details = {
      name = "C Major Triad",
      notes = {"C4", "E4", "G4"},
      midi = {60, 64, 67},
      complexity = 3
    }
  },
  {
    id = 2,
    chords = {"Am", "F", "C", "G"},
    details = {
      name = "A Minor Triad",
      notes = {"A3", "C4", "E4"},
      midi = {57, 60, 64},
      complexity = 4
    }
  }
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Progression identifier |
| `chords` | table | Lua table of chord symbol strings |
| `details.name` | string | First chord full name |
| `details.notes` | table | Note names with octaves |
| `details.midi` | table | MIDI note numbers (0-127) |
| `details.complexity` | integer | Harmonic complexity score |

## 5. Chord Symbol Format

### Supported Notation

chordify-agent recognizes standard chord symbols:

**Basic Triads:**
- Major: `C`, `G`, `F#`
- Minor: `Cm`, `Am`, `Bbm`
- Diminished: `Cdim`, `F#dim`
- Augmented: `Caug`, `Gaug`
- Power chords: `C5`, `G5`

**Extended Chords:**
- Dominant 7th: `C7`, `G7`
- Major 7th: `Cmaj7`, `Fmaj7`
- Minor 7th: `Cm7`, `Am7`
- Half-diminished: `Cm7b5`, `Bø7`
- Diminished 7th: `Cdim7`, `Bdim7`

**Alterations:**
- Suspended: `Csus2`, `Gsus4`
- Added notes: `Cadd9`, `Gadd11`
- Slash chords: `C/E`, `G/B`

**Notation Rules:**
1. Root note (A-G) + accidental (b/# optional)
2. Quality (m/dim/aug/maj optional)
3. Extensions (7/9/11/13 optional)
4. Alterations (sus/add/b5/etc. optional)

## 6. Usage Examples

### Example 1: Analyzing a Progression

```python
from chordify_agent import analyze_progression

progression = ["C", "Am", "F", "G"]
result = analyze_progression(progression)

print(result)
# {
#   "chord_names": ["C Major", "A Minor", "F Major", "G Major"],
#   "chord_count": 4,
#   "complexity_score": 4,
#   "common_patterns": ["I-vi-IV-V progression"]
# }
```

### Example 2: Browsing Dataset

```python
from chordify_agent import browse_dataset

results = browse_dataset(
    page=1,
    items_per_page=10,
    min_complexity=5,
    max_complexity=7
)

for prog in results['progressions']:
    print(f"ID {prog['id']}: {' - '.join(prog['chords'])}")
```

### Example 3: Exporting to REAPER

```python
from chordify_agent import export_lua_index

progressions = browse_dataset(page=1, items_per_page=100)
lua_code = export_lua_index(progressions['progressions'])

with open('chord_dataset_index.lua', 'w') as f:
    f.write(lua_code)
```

## See Also

- [examples/sample_progressions.json](../examples/sample_progressions.json) — Sample progression dataset
- [examples/song_structure.json](../examples/song_structure.json) — Full song structure example
- [README.md](../README.md) — Main documentation
- [Chord Recognition Algorithm](../chordify_agent/recognizer.py) — Implementation details

## References

- **Dataset:** Extended Groove MIDI Dataset (E-GMD) 1.2M progressions
- **Harmony Theory:** Berklee College of Music harmony curriculum
- **MIDI Standard:** General MIDI Level 1 specification
