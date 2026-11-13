"""Input validators for the lab exercises."""

from datetime import datetime
from numbers import Real


def validate_positive_number(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False, "Value must be a number"
    if value <= 0:
        return False, "Value must be greater than zero"
    return True, "Valid"


def validate_email(value):
    if not isinstance(value, str):
        return False, "Email must be a string"
    if " " in value:
        return False, "Email must not contain spaces"
    if "@" not in value:
        return False, "Email must contain @"
    local_part, domain = value.split("@", 1)
    if not local_part or "." not in domain:
        return False, "Email must contain a dot after @"
    if domain.startswith(".") or domain.endswith("."):
        return False, "Email must contain a valid domain"
    return True, "Valid"


def validate_username(value):
    if not isinstance(value, str):
        return False, "Username must be a string"
    if len(value) < 3:
        return False, "Username must be at least 3 characters"
    if len(value) > 20:
        return False, "Username must be at most 20 characters"
    if not value.isalnum():
        return False, "Username must contain only letters and numbers"
    return True, "Valid"


def validate_date(value):
    if not isinstance(value, str):
        return False, "Date must be a string"
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        if len(value) == 10 and value[4] == "-" and value[7] == "-":
            try:
                month = int(value[5:7])
                if not 1 <= month <= 12:
                    return False, "Invalid month"
            except ValueError:
                pass
        return False, "Date must be in YYYY-MM-DD format"
    return True, "Valid"
