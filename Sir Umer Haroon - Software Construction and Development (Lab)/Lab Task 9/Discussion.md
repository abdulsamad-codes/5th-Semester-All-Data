# Lab Task 9 Discussion

## Validation library

1. Boundary validation keeps invalid data out of the system, so the internal business logic can stay focused and does not repeat the same checks.
2. Separating validation from business logic lets each validator be tested independently and makes business-function tests smaller and easier to understand.
3. If a business function skips its validator, invalid data can reach the logic and cause incorrect results, unclear errors, or corrupted state.
4. Date validation was the hardest because it requires checking both the exact format and whether the calendar date actually exists.

## Resilient order service

1. Custom exceptions identify the category of failure, allowing the caller to handle invalid input differently from storage failure.
2. Processing continues so one bad order does not prevent valid orders later in the batch from being saved.
3. `InvalidOrderError` means the order data is unacceptable; `StorageError` means the data may be valid but persistence failed. The distinction supports accurate reporting and recovery.
4. The service could retry temporary failures, queue the order for later, or write it to a backup file/dead-letter queue.
5. The first failure would stop the batch and escape to the caller, so no complete summary would be returned.
