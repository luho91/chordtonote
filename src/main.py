import argparse
from root_extraction import extract_root_regex
from note_calc import *
from interval_maps import (TRIADS, SEVEN_CHORDS, NINE_CHORDS, ELEVEN_CHORDS, THIRTEEN_CHORDS)



def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(prog="chordtonote",
        description="Convert chord names to their note values.",
        usage="%(prog)s [options] <chord>",
        )
    # Add arguments
    parser.add_argument("chord", type=str, help="The chord name to convert (e.g., Cmaj7, D#m, F#dim).")
    parser.add_argument("-u", "--upper", action="store_true", help="Output the note names in uppercase.")
    # Parse arguments
    args = parser.parse_args()

    # merge all chord types into one dictionary for easy lookup
    chord_master_map = {**TRIADS, **SEVEN_CHORDS, **NINE_CHORDS, **ELEVEN_CHORDS, **THIRTEEN_CHORDS}
    chord_master_map[""] = chord_master_map["major"]  # default to major if no type specified

    #extract root note
    try:
        root_note = extract_root_regex(args.chord)
    except ValueError as e:
        print(e)
        return
    
    #calculate intervals based on chord type
    



if __name__ == "__main__":
    main()