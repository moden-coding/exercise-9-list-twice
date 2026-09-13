#!/usr/bin/env python3

import contextlib
import importlib
import io
import unittest
from unittest.mock import patch


def _expected_output(values):
    """Build the expected printed lines for a run of inputs.

    `values` is the sequence of numbers typed by the user, ending in the
    sentinel "0". After each non-terminating number is added to the running
    list, two lines are printed (the list as entered, and the list sorted).
    Once "0" is read, a final "Bye!" line is printed.
    """
    lines = []
    running = []
    for v in values[:-1]:
        running.append(int(v))
        lines.append(f"The list now: {running}")
        lines.append(f"The list in order: {sorted(running)}")
    return lines + ["Bye!"]


class TestListTwice(unittest.TestCase):
    """This assignment intentionally keeps its input loop at module level
    (the exercise explicitly forbids wrapping it in
    `if __name__ == "__main__":`, since the grader needs to re-run the loop
    with different inputs), so each test re-executes the module with
    importlib.reload() while patching builtins.input.

    Importing `src.list_twice` runs that loop for real the moment the
    module is first loaded, so even the *first* import must happen with
    input() already patched - otherwise it blocks on real stdin (or raises
    EOFError if stdin is closed) before any test body runs. setUpClass
    performs that first guarded import; every test then reloads the
    already-imported module under its own patch.
    """

    @classmethod
    def setUpClass(cls):
        with patch('builtins.input', side_effect=["0"]):
            cls.list_twice = importlib.import_module('src.list_twice')

    def run_with_inputs(self, values):
        with patch('builtins.input', side_effect=list(values)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                importlib.reload(self.list_twice)
            return buf.getvalue()

    def check_inputs(self, values):
        output = self.run_with_inputs(values)
        expected_lines = _expected_output(values)
        # Split on stripped output so a trailing newline from the final
        # print() doesn't produce a spurious extra blank "line" - the
        # test cares about what was printed, not incidental whitespace.
        output_lines = [
            line.strip() for line in output.strip().split("\n")
        ]

        self.assertTrue(
            len(output.strip()) > 0,
            msg="Your program does not print out anything with the input "
                "%s." % (values,))
        self.assertEqual(
            output_lines, expected_lines,
            msg="For input %s, your program should print out:\n%s\n"
                "but it printed:\n%s"
                % (values, "\n".join(expected_lines), "\n".join(output_lines)))

    def test_inputs_1_2_3_0(self):
        self.check_inputs(tuple("1 2 3 0".split()))

    def test_inputs_9_8_7_0(self):
        self.check_inputs(tuple("9 8 7 0".split()))

    def test_inputs_many_values(self):
        self.check_inputs(tuple("9 1 8 2 7 3 11 12 22 21 0".split()))


if __name__ == '__main__':
    unittest.main()
