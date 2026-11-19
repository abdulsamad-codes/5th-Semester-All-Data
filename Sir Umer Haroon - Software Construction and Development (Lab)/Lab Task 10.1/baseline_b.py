import csv
import os
import time


NUM_FILES = 12
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "inputs")


def main():
    start = time.perf_counter()

    for file_id in range(NUM_FILES):
        path = os.path.join(INPUT_DIR, f"data_{file_id:02d}.csv")
        total_value = 0.0
        category_counts = {"A": 0, "B": 0, "C": 0}

        with open(path, "r", newline="", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                total_value += float(row["value"])
                category = row["category"]
                category_counts[category] += 1

        print(
            f"{os.path.basename(path)}: "
            f"total_value={total_value:.3f}, category_counts={category_counts}"
        )

    elapsed = time.perf_counter() - start
    print(f"Total wall-clock time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

# Sequential processing takes 67 seconds.
# The requirement is 480 seconds (8 minutes).
# Therefore sequential meets the requirement.