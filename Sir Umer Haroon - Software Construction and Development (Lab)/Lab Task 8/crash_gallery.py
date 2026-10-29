"""SCD Lab Task 8, Task 1. Run: python crash_gallery.py

The original functions are preserved verbatim in ORIGINAL_SOURCE.
The public functions below are the patched versions.
"""

import math
import os
import sys
import tempfile
from pathlib import Path


ORIGINAL_SOURCE = '''def divide(a, b):
    return a / b

def get_first(items):
    return items[0]

def get_age(person):
    return person["age"]

def parse_number(text):
    return int(text)

def read_file(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content

def average(numbers):
    return sum(numbers) / len(numbers)
'''

original = {}
exec(ORIGINAL_SOURCE, original)


def is_number(value):
    """Reject booleans, nonnumeric values, NaN and infinity."""
    return type(value) is int or (type(value) is float and math.isfinite(value))


def divide(a, b):
    if not is_number(a) or not is_number(b):
        return "Error: both arguments must be finite numbers"
    if b == 0:
        return "Error: cannot divide by zero"
    return a / b


def get_first(items):
    if not isinstance(items, list):
        return "Error: input is not a list"
    if not items:
        return "Error: list is empty"
    return items[0]


def get_age(person):
    if not isinstance(person, dict):
        return "Error: input is not a dictionary"
    if "age" not in person:
        return "Error: missing age"
    if type(person["age"]) is not int or person["age"] < 0:
        return "Error: age must be a nonnegative integer"
    return person["age"]


def parse_number(text):
    # Guard the conversion with checks rather than catching conversion errors.
    if not isinstance(text, str):
        return "Error: input must be text"
    cleaned = text.strip()
    digits = cleaned[1:] if cleaned[:1] in ("+", "-") else cleaned
    if not digits or any(char not in "0123456789" for char in digits):
        return "Error: not a number"
    limit = sys.get_int_max_str_digits() if hasattr(sys, "get_int_max_str_digits") else 0
    if limit and len(digits) > limit:
        return "Error: number has too many digits"
    return int(cleaned)


def read_file(filename):
    if not isinstance(filename, str) or not filename.strip() or "\x00" in filename:
        return "Error: filename must be nonempty text without null characters"
    if not os.path.exists(filename):
        return "Error: file not found"
    if not os.path.isfile(filename):
        return "Error: path is not a regular file"
    # Checks cannot prevent a file being removed or permissions changing before
    # open(). A narrow I/O handler is necessary for those environmental failures.
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeError:
        return "Error: file is not valid UTF-8 text"
    except OSError:
        return "Error: file could not be read"


def average(numbers):
    if not isinstance(numbers, list):
        return "Error: input is not a list"
    if not numbers:
        return "Error: cannot average an empty list"
    if any(not is_number(number) for number in numbers):
        return "Error: every item must be a finite number"
    return sum(numbers) / len(numbers)


def collect_results():
    """Record real original errors and assert every patched expected result."""
    rows = []
    with tempfile.TemporaryDirectory(prefix="crash_gallery_", dir=Path(__file__).resolve().parent) as folder:
        missing = str(Path(folder) / "missing.txt")
        sample = Path(folder) / "sample.txt"
        sample.write_text("Hello, lab!", encoding="utf-8")
        cases = [
            ("divide", (10, 0), "Error: cannot divide by zero", True),
            ("divide", ("10", 2), "Error: both arguments must be finite numbers", True),
            ("divide", (10, None), "Error: both arguments must be finite numbers", True),
            ("divide", (10, 2), 5.0, False),
            ("get_first", ([],), "Error: list is empty", True),
            ("get_first", (None,), "Error: input is not a list", True),
            ("get_first", (42,), "Error: input is not a list", True),
            ("get_first", ([7, 8],), 7, False),
            ("get_age", ({},), "Error: missing age", True),
            ("get_age", ("Ali",), "Error: input is not a dictionary", True),
            ("get_age", (None,), "Error: input is not a dictionary", True),
            ("get_age", ({"age": -1},), "Error: age must be a nonnegative integer", True),
            ("get_age", ({"age": 20},), 20, False),
            ("parse_number", ("abc",), "Error: not a number", True),
            ("parse_number", (None,), "Error: input must be text", True),
            ("parse_number", ("3.5",), "Error: not a number", True),
            ("parse_number", ("",), "Error: not a number", True),
            ("parse_number", (" -12 ",), -12, False),
            ("read_file", (missing,), "Error: file not found", True),
            ("read_file", (None,), "Error: filename must be nonempty text without null characters", True),
            ("read_file", (folder,), "Error: path is not a regular file", True),
            ("read_file", (str(sample),), "Hello, lab!", False),
            ("average", ([],), "Error: cannot average an empty list", True),
            ("average", (["a", "b"],), "Error: every item must be a finite number", True),
            ("average", (None,), "Error: input is not a list", True),
            ("average", ([10, 20, 30],), 20.0, False),
        ]
        for name, args, expected, bad in cases:
            try:
                before = repr(original[name](*args))
                error_type = "None"
            except Exception as error:
                before = str(error)
                error_type = type(error).__name__
            actual = globals()[name](*args)
            assert actual == expected, (name, args, actual, expected)
            label = name + "(" + ", ".join(repr(arg) for arg in args) + ")"
            for value, replacement in ((missing, "missing.txt"), (str(sample), "sample.txt"), (folder, "<directory>")):
                # Normalize only temporary paths for a readable report.
                label = label.replace(repr(value), repr(replacement))
                before = before.replace(value, replacement).replace(value.replace("\\", "\\\\"), replacement)
            rows.append(dict(function=name, call=label, bad=bad, original=before,
                             error_type=error_type, expected=repr(expected), patched=repr(actual), passed=True))
    return rows


if __name__ == "__main__":
    results = collect_results()
    for row in results:
        print(row["call"])
        print("  Original:", row["error_type"], row["original"])
        print("  Patched: ", row["patched"], "[PASS]")
    print(f"\n{len(results)}/{len(results)} patched checks passed.")
