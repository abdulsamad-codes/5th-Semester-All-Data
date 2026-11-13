"""Test harness for the validation and business-logic modules."""

from logic import create_account, schedule_event, send_email
from validators import (
    validate_date,
    validate_email,
    validate_positive_number,
    validate_username,
)


def _show(label, function, *args):
    try:
        result = function(*args)
        print(f"{label} -> {result!r}")
    except ValueError as error:
        print(f"{label} -> ValueError: {error}")


def run_tests():
    cases = [
        ("validate_positive_number(5)", validate_positive_number, 5),
        ("validate_positive_number(-5)", validate_positive_number, -5),
        ("validate_positive_number('abc')", validate_positive_number, "abc"),
        ("validate_email('ali@example.com')", validate_email, "ali@example.com"),
        ("validate_email('not an email')", validate_email, "not an email"),
        ("validate_username('ali123')", validate_username, "ali123"),
        ("validate_username('al')", validate_username, "al"),
        ("validate_date('2024-10-05')", validate_date, "2024-10-05"),
        ("validate_date('2024-13-05')", validate_date, "2024-13-05"),
        ("create_account('ali123', 100)", create_account, "ali123", 100),
        ("create_account('al', 100)", create_account, "al", 100),
        ("create_account('ali123', -50)", create_account, "ali123", -50),
        ("send_email('ali@example.com', 'Hello')", send_email, "ali@example.com", "Hello"),
        ("send_email('not an email', 'Hello')", send_email, "not an email", "Hello"),
        ("schedule_event('2024-10-05', 'Lab')", schedule_event, "2024-10-05", "Lab"),
        ("schedule_event('2024-13-05', 'Lab')", schedule_event, "2024-13-05", "Lab"),
    ]
    for label, function, *args in cases:
        _show(label, function, *args)


if __name__ == "__main__":
    run_tests()
