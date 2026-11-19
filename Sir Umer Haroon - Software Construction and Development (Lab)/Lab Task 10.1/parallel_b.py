import csv
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


MAX_WORKERS = 4
NUM_FILES = 12
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "inputs")
CHECKPOINT_PATH = os.path.join(SCRIPT_DIR, "checkpoint.json")
CHECKPOINT_TMP_PATH = os.path.join(SCRIPT_DIR, "checkpoint.json.tmp")


def process_file(path):
    total_value = 0.0
    category_counts = {"A": 0, "B": 0, "C": 0}

    with open(path, "r", newline="", encoding="utf-8") as input_file:
        for row in csv.DictReader(input_file):
            total_value += float(row["value"])
            category_counts[row["category"]] += 1

    return {
        "file": path,
        "total_value": total_value,
        "category_counts": category_counts,
    }


def load_checkpoint():
    if not os.path.exists(CHECKPOINT_PATH):
        return {}
    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as checkpoint_file:
        return json.load(checkpoint_file)


def save_checkpoint(checkpoint):
    with open(CHECKPOINT_TMP_PATH, "w", encoding="utf-8") as checkpoint_file:
        json.dump(checkpoint, checkpoint_file, indent=2)
        checkpoint_file.flush()
        os.fsync(checkpoint_file.fileno())
    os.replace(CHECKPOINT_TMP_PATH, CHECKPOINT_PATH)


def main():
    start = time.perf_counter()
    checkpoint = load_checkpoint()
    paths = [
        os.path.join(INPUT_DIR, f"data_{file_id:02d}.csv")
        for file_id in range(NUM_FILES)
    ]
    remaining = [
        path for path in paths if os.path.basename(path) not in checkpoint
    ]

    print(
        f"Processing {len(remaining)} file(s); "
        f"{len(paths) - len(remaining)} already checkpointed"
    )

    try:
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_file, path): path for path in remaining}
            for future in as_completed(futures):
                result = future.result()
                checkpoint[os.path.basename(result["file"])] = result
                save_checkpoint(checkpoint)
                print(f"Checkpointed {os.path.basename(result['file'])}")
    except KeyboardInterrupt:
        print("Interrupted; completed files remain safely checkpointed.")

    total_value = sum(result["total_value"] for result in checkpoint.values())
    category_counts = {"A": 0, "B": 0, "C": 0}
    for result in checkpoint.values():
        for category in category_counts:
            category_counts[category] += result["category_counts"][category]

    elapsed = time.perf_counter() - start
    print(f"Combined total_value={total_value:.3f}")
    print(f"Combined category_counts={category_counts}")
    print(f"Total wall-clock time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
