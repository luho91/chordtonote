import unittest
import sys
from io import StringIO
from main import main
from root_extraction import extract_root_regex
from note_calc import calculate_notes, get_note_names
from interval_maps import NOTE_TO_INT, INT_TO_NOTES


class TestChordToNote(unittest.TestCase):

    # root extraction tests
    def test_extract_root_regex_basic(self):
        root, quality, slash = extract_root_regex("C")
        self.assertEqual(root, "C")
        self.assertEqual(quality, "")
        self.assertEqual(slash, "")

    def test_extract_root_regex_minor(self):
        root, quality, slash = extract_root_regex("Cm")
        self.assertEqual(root, "C")
        self.assertEqual(quality, "m")
        self.assertEqual(slash, "")

    def test_extract_root_regex_seventh(self):
        root, quality, slash = extract_root_regex("C7")
        self.assertEqual(root, "C")
        self.assertEqual(quality, "7")
        self.assertEqual(slash, "")

    def test_extract_root_regex_sharp(self):
        root, quality, slash = extract_root_regex("C#")
        self.assertEqual(root, "C#")
        self.assertEqual(quality, "")
        self.assertEqual(slash, "")

    def test_extract_root_regex_flat(self):
        root, quality, slash = extract_root_regex("Db")
        self.assertEqual(root, "Db")
        self.assertEqual(quality, "")
        self.assertEqual(slash, "")

    def test_extract_root_regex_slash(self):
        root, quality, slash = extract_root_regex("C/G")
        self.assertEqual(root, "C")
        self.assertEqual(quality, "")
        self.assertEqual(slash, "G")

    def test_extract_root_regex_complex(self):
        root, quality, slash = extract_root_regex("F#m7/D#")
        self.assertEqual(root, "F#")
        self.assertEqual(quality, "m7")
        self.assertEqual(slash, "D#")

    def test_extract_root_regex_lowercase(self):
        root, quality, slash = extract_root_regex("cm7")
        self.assertEqual(root, "c")
        self.assertEqual(quality, "m7")
        self.assertEqual(slash, "")

    def test_extract_root_regex_invalid(self):
        with self.assertRaises(ValueError):
            extract_root_regex("H")


    # note calculation tests
    def test_calculate_notes_major(self):
        pitches = list(calculate_notes("C", [0, 4, 7]))
        self.assertEqual(pitches, [0, 4, 7])

    def test_calculate_notes_minor(self):
        pitches = list(calculate_notes("A", [0, 3, 7]))
        self.assertEqual(pitches, [9, 0, 4])  # A=9, C=0, E=4

    def test_calculate_notes_sharp(self):
        pitches = list(calculate_notes("F#", [0, 4, 7]))
        self.assertEqual(pitches, [6, 10, 1])  # F#=6, A#=10, C#=1

    def test_calculate_notes_flat(self):
        pitches = list(calculate_notes("Bb", [0, 4, 7]))
        self.assertEqual(pitches, [10, 2, 5])  # Bb=10, D=2, F=5

    def test_calculate_notes_invalid_root(self):
        with self.assertRaises(ValueError):
            list(calculate_notes("H", [0, 4, 7]))


    # Note names tests
    def test_get_note_names_major(self):
        pitches = [0, 4, 7]
        names = list(get_note_names(pitches, "C", ""))
        self.assertEqual(names, ["C", "E", "G"])

    def test_get_note_names_minor(self):
        pitches = [0, 3, 7]
        names = list(get_note_names(pitches, "C", "minor"))
        self.assertEqual(names, ["C", "Eb", "G"])

    def test_get_note_names_sharp_root(self):
        pitches = [6, 10, 1]
        names = list(get_note_names(pitches, "F#", "major"))
        self.assertEqual(names, ["F#", "A#", "C#"])

    def test_get_note_names_flat_root(self):
        pitches = [10, 2, 5]
        names = list(get_note_names(pitches, "Bb", "major"))
        self.assertEqual(names, ["Bb", "D", "F"])

    def test_get_note_names_enharmonic_conflict(self):
        # Note: The code prioritizes sharps over flats, so no conflict raised
        pitches = [1, 4, 7]
        names = list(get_note_names(pitches, "C#", "dim"))
        self.assertEqual(names, ["C#", "E", "G"])  # Uses sharps


    # main() tests
    def test_main_basic(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "C"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: C", output)
            self.assertIn("Notes: C E G", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_minor(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "Cm"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: Cm", output)
            self.assertIn("Notes: C Eb G", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_seventh(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "C7"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: C7", output)
            self.assertIn("Notes: C E G A#", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_sharp_minor_seventh(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "F#m7"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: F#m7", output)
            self.assertIn("Notes: F# A C# E", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_slash_chord(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "Gm/E"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: Gminor/E", output)
            self.assertIn("Notes: E G Bb D", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_unknown_quality(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "Cxyz"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Error: Unknown chord quality: xyz", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_invalid_root(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "H"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Error: Invalid chord format: H", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_case_insensitive(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "cm7"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: cm7", output)
            self.assertIn("Notes: C Eb G Bb", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_double_accidental_root(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "C##"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Error: That's not a note bruh. A-G only.", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_quality_with_numbers(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "C9"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: C9", output)
            self.assertIn("Notes: C E G A# D", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_augmented(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "Caug"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: Caug", output)
            self.assertIn("Notes: C E G#", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_diminished(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "bdIm"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: bdim", output)
            self.assertIn("Notes: B D F", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_power_chord(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "C5"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: C5", output)
            self.assertIn("Notes: C G", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_slash_with_sharp(self):
        old_argv = sys.argv
        sys.argv = ["main.py", "F#/C#"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Chord: F#major/C#", output)
            self.assertIn("Notes: C# F# A#", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_empty_chord(self):
        old_argv = sys.argv
        sys.argv = ["main.py", ""]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Error: Invalid chord format:", output)
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv

    def test_main_no_args(self):
        old_argv = sys.argv
        sys.argv = ["main.py"]
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with self.assertRaises(SystemExit):
                main()
        finally:
            sys.stdout = sys.__stdout__
            sys.argv = old_argv


if __name__ == "__main__":
    unittest.main()