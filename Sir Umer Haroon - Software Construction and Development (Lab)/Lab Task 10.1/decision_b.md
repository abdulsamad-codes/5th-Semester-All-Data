# Scenario B.5 - Decision Document

## Results table

Run `python compare_b.py` and copy its three measured times into this table.

| Mechanism | Time (seconds) | Result |
|---|---:|---|
| Sequential | ___ | 12 files processed |
| Threads | ___ | 12 files processed |
| Processes | ___ | 12 files processed |

## Decisions

1. **Requirement:** The sequential baseline took ___ seconds. It therefore
   **did / did not** meet the 480-second requirement.
2. **Baseline:** The sequential result was the reference measurement; the
   parallel versions were compared against this same workload.
3. **Mechanism:** Processes were selected because the work is CPU-bound and
   `ProcessPoolExecutor` can use multiple Python processes without the
   limitation of the GIL.
4. **Failure design:** If a worker crashes, completed results remain in the
   atomically written checkpoint. A later run skips those files and processes
   only the missing files.
5. **Final decision:** The process-pool version is preferred when the measured
   process time is lower than the sequential time; otherwise the sequential
   version is the simpler valid choice for this workload.
