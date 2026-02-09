
from interval_maps import CHROMATIC

def calculate_notes(base_note, intervals):
    """Get the note names for a given base note and intervals."""
    base_value = CHROMATIC[base_note]
    for interval in intervals:
        if interval < 0 or interval > 13:
            raise ValueError(f"Invalid interval: {interval}. Must be between 0 and 13.")
        yield (base_value + interval) % 12 # return pitch classes as integers for now, will map to names later

def get_note_names(pitch_classes, root):
    """Map the calculated note values back to their names ENHARMONICALLY CORRECT."""
    # Determine if the root note contains sharps or flats to guide selection of enharmonic equivalents
    use_flats = "b" in root
    use_sharps = "#" in root
    if use_flats and use_sharps:
            raise ValueError(f"Invalid root note: {root}. Cannot contain both sharps and flats.")
    # If neither sharps nor flats are present, default to natural notes, but allow for accidental selection if necessary
    for pitch in pitch_classes:
        options = CHROMATIC[pitch] # for based O(1) lookup
        if use_flats:
             selection = next((note for note in options if "b" in note),
                               next(note for note in options if len(note) == 1), options[0])
        elif use_sharps:
             selection = next((note for note in options if "#" in note),
                               next(note for note in options if len(note) == 1), options[0])
        else:
             selection = next((note for note in options if len(note) == 1), options[0])
        
        yield selection