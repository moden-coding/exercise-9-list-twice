#!/usr/bin/env python3

import contextlib
import importlib
import io
import unittest
from unittest.mock import patch

from src import list_twice


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
    """

    def run_with_inputs(self, values):
        with patch('builtins.input', side_effect=list(values)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                importlib.reload(list_twice)
            return buf.getvalue()

    def check_inputs(self, values):
        output = self.run_with_inputs(values)
        expected_lines = _expected_output(values)
        output_lines = output.split("\n")

        self.assertTrue(
            len(output.strip()) > 0,
            msg="Your program does not print out anything with the input "
                "%s." % (values,))
        self.assertEqual(
            len(output_lines), len(expected_lines),
            msg="In addition to asking for the inputs from the user, your "
                "program should print out %d rows for input %s (one 'The "
                "list now'/'The list in order' pair per number entered, "
                "plus a final 'Bye!'); it printed %d rows."
                % (len(expected_lines), values, len(output_lines)))
        for row, (actual, expected) in enumerate(
                zip(output_lines, expected_lines), start=1):
            self.assertEqual(
                actual.strip(), expected,
                msg="On row %d, your program should print out\n%s\nbut it "
                    "printed\n%s\nwhen the input is %s."
                    % (row, expected, actual, values))

    def test_inputs_1_2_3_0(self):
        self.check_inputs(tuple("1 2 3 0".split()))

    def test_inputs_9_8_7_0(self):
        self.check_inputs(tuple("9 8 7 0".split()))

    def test_inputs_many_values(self):
        self.check_inputs(tuple("9 1 8 2 7 3 11 12 22 21 0".split()))


if __name__ == '__main__':
    unittest.main()
