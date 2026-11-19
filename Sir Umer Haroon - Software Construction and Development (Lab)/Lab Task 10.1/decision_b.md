# Scenario B.5 - Decision Document

## Results table

| Mechanism | Time (seconds) | Result |
|---|---:|---|
| Sequential | 72.698698 | 12 files processed |
| Threads | 72.532353 | 12 files processed |
| Processes | 19.889391 | 12 files processed |

## Decisions

1. **Requirement:** The sequential baseline took 72.698698 seconds, so it
   did meet the 480-second requirement.
2. **Baseline:** The sequential result was the reference measurement. Threads
   were only 0.166345 seconds faster, while processes were 52.809307 seconds
   faster, or about 3.65 times faster than sequential.
3. **Mechanism:** Processes were selected for the faster measurement because
   the work is CPU-bound and separate Python processes avoid the GIL.
4. **Failure design:** If a worker crashes, completed results remain in the
   atomically written checkpoint. A later run skips those files and processes
   only the missing files.
5. **Final decision:** Sequential processing is already sufficient for the
   stated requirement and is the simplest solution. The process-pool version
   is preferred when shorter runtime and restartability are important enough
   to justify its extra implementation complexity.
