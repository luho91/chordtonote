import re


def extract_root_regex(chord):
    # Group 1: Root ([A-G][#b]*)
    # Group 2: Quality (.*?) - Non-greedy to allow slash detection
    # Group 3: Optional Slash Note (?:/([A-G][#b]*))?
    pattern = r"^([A-G][#b]*)(.*?)(?:/([A-G][#b]*))?$"
    match = re.match(pattern, chord, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid chord format: {chord}")
    root, quality, slash_note = match.groups()
    if quality is None:
        quality = ""  # default to major if no quality specified
    if slash_note is None:
        slash_note = ""  # default to no slash if not specified

    return root, quality, slash_note