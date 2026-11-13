"""Business functions that validate inputs at their boundary."""

from validators import (
    validate_date,
    validate_email,
    validate_positive_number,
    validate_username,
)


def _require_valid(result):
    valid, message = result
    if not valid:
        raise ValueError(message)


def create_account(username, initial_deposit):
    _require_valid(validate_username(username))
    _require_valid(validate_positive_number(initial_deposit))
    return {"username": username, "balance": initial_deposit}


def send_email(email, message):
    _require_valid(validate_email(email))
    return f"Email sent to {email}: {message}"


def schedule_event(date, event_name):
    _require_valid(validate_date(date))
    return {"date": date, "event": event_name}
