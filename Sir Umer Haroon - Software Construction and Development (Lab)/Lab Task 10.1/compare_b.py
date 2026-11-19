import csv
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


MAX_WORKERS = 4
NUM_FILES = 12
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "inputs")


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


def file_paths():
    return [
        os.path.join(INPUT_DIR, f"data_{file_id:02d}.csv")
        for file_id in range(NUM_FILES)
    ]


def run_sequential(paths):
    return [process_file(path) for path in paths]


def run_with_executor(executor_class, paths):
    with executor_class(max_workers=MAX_WORKERS) as executor:
        return list(executor.map(process_file, paths))


def measure(label, function, paths):
    start = time.perf_counter()
    results = function(paths)
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.6f} seconds ({len(results)} files)")
    return elapsed


def main():
    paths = file_paths()
    print("Mechanism                 Time (s)")
    print("-----------------------------------")
    sequential_time = measure("Sequential", run_sequential, paths)
    thread_time = measure(
        "Threads", lambda items: run_with_executor(ThreadPoolExecutor, items), paths
    )
    process_time = measure(
        "Processes", lambda items: run_with_executor(ProcessPoolExecutor, items), paths
    )
    print()
    print(f"Sequential baseline: {sequential_time:.6f} seconds")
    print(f"Threads: {thread_time:.6f} seconds")
    print(f"Processes: {process_time:.6f} seconds")


if __name__ == "__main__":
    main()
