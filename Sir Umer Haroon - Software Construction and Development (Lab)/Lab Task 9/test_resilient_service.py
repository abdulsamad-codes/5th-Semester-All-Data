"""Scenario harness for the resilient order service."""

import tempfile
from pathlib import Path

from resilient_service import process_orders


def run_scenarios():
    with tempfile.TemporaryDirectory() as temporary_directory:
        output_file = Path(temporary_directory) / "orders.txt"
        scenarios = [
            (
                "all valid",
                [{"id": 1, "amount": 100}, {"id": 2, "amount": 50}, {"id": 3, "amount": 25}],
                output_file,
            ),
            (
                "some invalid",
                [
                    {"id": 1, "amount": 100},
                    {"amount": 50},
                    {"id": 3, "amount": -25},
                    {"id": 4, "amount": "25"},
                ],
                output_file,
            ),
            (
                "unwritable file",
                [{"id": 1, "amount": 100}, {"id": 2, "amount": 50}],
                Path(temporary_directory) / "missing" / "orders.txt",
            ),
            (
                "mixed",
                [{"id": 1, "amount": 100}, {"id": 2, "amount": -5}, {"id": 3, "amount": 25}, {"amount": 10}],
                output_file,
            ),
        ]
        for number, (name, orders, filename) in enumerate(scenarios, start=1):
            print(f"Scenario {number}: {name}")
            print(process_orders(orders, filename))
            print()


if __name__ == "__main__":
    run_scenarios()
