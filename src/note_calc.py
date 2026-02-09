
from interval_maps import CHROMATIC


def calculate_notes(base_note, intervals):
    """Get the note names for a given base note and intervals."""
    base_value = CHROMATIC[base_note]
    for interval in intervals:
        if interval < 0 or interval > 13:
            raise ValueError(f"Invalid interval: {interval}. Must be between 0 and 13.")
        yield (base_value + interval) % 12

def get_note_names(pitch_classes):
    """Map the calculated note values back to their names."""
    for pitch in pitch_classes:
        yield CHROMATIC.get(pitch, "Unknown")
        

