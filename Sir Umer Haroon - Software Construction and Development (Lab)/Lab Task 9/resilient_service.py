"""Resilient order processing service."""

import json


class InvalidOrderError(Exception):
    pass


class StorageError(Exception):
    pass


def validate_order(order):
    if not isinstance(order, dict):
        raise InvalidOrderError("order must be a dictionary")
    if "id" not in order:
        raise InvalidOrderError("missing id")
    if "amount" not in order:
        raise InvalidOrderError("missing amount")
    amount = order["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise InvalidOrderError("amount must be a number")
    if amount <= 0:
        raise InvalidOrderError("amount must be positive")


def save_order(order, filename):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(json.dumps(order) + "\n")
    except (OSError, TypeError, ValueError) as error:
        raise StorageError(f"cannot write to {filename}") from error
    return True


def process_orders(orders, filename):
    summary = {"success": 0, "failed": 0, "errors": []}
    for order in orders:
        try:
            validate_order(order)
            save_order(order, filename)
            summary["success"] += 1
        except InvalidOrderError as error:
            summary["failed"] += 1
            summary["errors"].append(f"Invalid order: {error}")
        except StorageError as error:
            summary["failed"] += 1
            summary["errors"].append(f"Storage error: {error}")
    return summary
