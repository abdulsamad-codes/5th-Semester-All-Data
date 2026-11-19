import csv
import os
import random

# 2,000,000 rows per file — enough to be genuinely CPU-bound on any laptop,
# small enough that generation finishes in a couple of minutes.
ROWS_PER_FILE = 2_000_000
NUM_FILES = 12
OUTPUT_DIR = "inputs"


def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    random.seed(42)  # deterministic: every student gets identical files

    for file_id in range(NUM_FILES):
        path = os.path.join(OUTPUT_DIR, f"data_{file_id:02d}.csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "value", "category"])
            for row in range(ROWS_PER_FILE):
                writer.writerow([
                    row,
                    round(random.random() * 1000, 3),
                    random.choice(["A", "B", "C"]),
                ])
        print(f"wrote {path}")


if __name__ == "__main__":
    generate()