import re


def extract_root_regex(chord):
    # Pattern: ^[A-G] matches starting note, [#b]* matches zero or more accidentals
    pattern = r"^[A-G][#b]*"
    match = re.match(pattern, chord, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid chord format: {chord}")
    root, quality = match.groups()
    return root.upper(), quality.lower() if quality else ""