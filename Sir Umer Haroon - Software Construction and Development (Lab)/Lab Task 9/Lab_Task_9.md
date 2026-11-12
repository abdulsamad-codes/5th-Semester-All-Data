# SCD Lab Task 9

**Course:** Software Construction and Development, Lab (Sec A), IMSciences Peshawar
**Teacher:** Muhammad Umer Haroon
**Classroom post:** Lab Task 9 (100 points, due 12 Nov 2026, 8:30)
**Source:** `Lab Task 9.pdf` attached to the post. The post itself has no other text. The PDF is 6 pages and contains two tasks: the validation library, then a second task titled "Next Task".

> Formatting note: the PDF text came out with its line breaks and code indentation flattened. I restored the layout of the code samples and of the expected output, and fixed three spots where a word was split across a line break ("a mount", "d irectory", "t xt" are "amount", "directory", "txt"). The wording is otherwise unchanged.

---

## Task 1: Defensive validation library

You will build a small library of defensive functions that follow the patterns from the previous lecture. The library will handle input validation at the boundary, use clear error messages, and separate validation from logic.

The key idea is that each function should do one thing well, and validation should happen once at the boundary, not scattered throughout the code.

### What to Do

#### Part A: Build the Validation Module

Create a file called `validators.py`. Write the following validation functions, each doing one task.

- `validate_positive_number` takes a value and returns a tuple of a boolean and a message. It checks that the value is a number and greater than zero.
- `validate_email` takes a string and returns a tuple of a boolean and a message. It checks that the string contains an at sign, a dot after the at sign, and no spaces.
- `validate_username` takes a string and returns a tuple of a boolean and a message. It checks that the string is between three and twenty characters and contains only letters and numbers.
- `validate_date` takes a string and returns a tuple of a boolean and a message. It checks that the string matches the format YYYY-MM-DD and represents a real date.

Here is a sample of what one function should look like.

```python
def validate_positive_number(value):
    if not isinstance(value, (int, float)):
        return False, "Value must be a number"
    if value <= 0:
        return False, "Value must be greater than zero"
    return True, "Valid"
```

#### Part B: Build the Business Logic Module

Create a file called `logic.py`. Write the following functions. Each function should call the appropriate validator at the start and raise a `ValueError` if validation fails. After validation, the function should trust the input and do its work without further checks.

- `create_account` takes a username and an initial deposit. It validates both and returns a dictionary with the username and balance.
- `send_email` takes an email address and a message. It validates the email and returns a confirmation string.
- `schedule_event` takes a date and an event name. It validates the date and returns a dictionary with the event details.

#### Part C: Build the Test Harness

Create a file called `test_library.py`. Write a function called `run_tests` that calls each validator and each business function with both valid and invalid input. Print the result of each call in a clear format.

Your output should look like this.

```text
validate_positive_number(5) -> (True, 'Valid')
validate_positive_number(-5) -> (False, 'Value must be greater than zero')
validate_positive_number('abc') -> (False, 'Value must be a number')
validate_email('ali@example.com') -> (True, 'Valid')
validate_email('not an email') -> (False, 'Email must contain @')
validate_username('ali123') -> (True, 'Valid')
validate_username('al') -> (False, 'Username must be at least 3 characters')
validate_date('2024-10-05') -> (True, 'Valid')
validate_date('2024-13-05') -> (False, 'Invalid month')

create_account('ali123', 100) -> {'username': 'ali123', 'balance': 100}
create_account('al', 100) -> ValueError: Username must be at least 3 characters
create_account('ali123', -50) -> ValueError: Value must be greater than zero
```

#### Part D: Discussion

Write short answers to these questions.

1. Why is it better to validate at the boundary rather than inside every function.
2. How does separating validation from business logic make the code easier to test.
3. What would happen if you forgot to call the validator in one of the business functions.
4. Which function was hardest to validate, and why.

---

## Next Task: Resilient order service

### Background

Now that you understand exception handling, you will build a small service that is resilient to failures. The service will process a list of orders, save each valid order to a file, and produce a summary of successes and failures. It must handle missing files, malformed data, and unexpected errors without crashing.

The key idea is that exception handling should catch specific errors at the place where something useful can be done, not everywhere and not nowhere.

### What to Do

#### Part A: Define Custom Exceptions

Create a file called `resilient_service.py`. Define two custom exceptions at the top.

```python
class InvalidOrderError(Exception):
    pass

class StorageError(Exception):
    pass
```

#### Part B: Build the Order Processor

Write the following functions, each doing one task.

- `validate_order` takes an order and raises `InvalidOrderError` if the order is not a dictionary, if it is missing the `id` or `amount` key, if the amount is not a number, or if the amount is not positive. Otherwise it returns `None`.
- `save_order` takes an order and a filename and raises `StorageError` if the file cannot be written. It uses the `with` statement. On success it returns `True`.
- `process_orders` takes a list of orders and a filename and returns a summary dictionary with three keys: `success`, `failed`, and `errors`. For each order, it calls `validate_order`, then `save_order`. If either raises an exception, it catches it, records the reason in the errors list, and continues to the next order.

Here is a sample of what `process_orders` should look like.

```python
def process_orders(orders, filename):
    summary = {"success": 0, "failed": 0, "errors": []}
    for order in orders:
        try:
            validate_order(order)
            save_order(order, filename)
            summary["success"] += 1
        except InvalidOrderError as e:
            summary["failed"] += 1
            summary["errors"].append(f"Invalid order: {e}")
        except StorageError as e:
            summary["failed"] += 1
            summary["errors"].append(f"Storage error: {e}")
    return summary
```

#### Part C: Build the Test Harness

Create a function called `run_scenarios` that calls `process_orders` with at least four different scenarios.

1. The first scenario contains all valid orders.
2. The second scenario contains some invalid orders, such as a missing id, a negative amount, and a string amount.
3. The third scenario uses a filename that cannot be written, such as `/nonexistent/directory/orders.txt`, to test the storage error path.
4. The fourth scenario contains a mix of valid and invalid orders to confirm that processing continues after a failure.

Print the summary for each scenario.

Your output should look like this.

```text
Scenario 1: all valid
{'success': 3, 'failed': 0, 'errors': []}

Scenario 2: some invalid
{'success': 1, 'failed': 3, 'errors': ['Invalid order: missing id', 'Invalid order: amount must be positive', 'Invalid order: amount must be a number']}

Scenario 3: unwritable file
{'success': 0, 'failed': 2, 'errors': ['Storage error: cannot write to /nonexistent/directory/orders.txt', 'Storage error: cannot write to /nonexistent/directory/orders.txt']}

Scenario 4: mixed
{'success': 2, 'failed': 2, 'errors': ['Invalid order: amount must be positive', 'Invalid order: missing id']}
```

#### Part D: Reflection

Write short answers to these questions.

1. Why are custom exceptions better than using plain `Exception` in this scenario.
2. Why does `process_orders` continue after an error instead of stopping.
3. What is the difference between `InvalidOrderError` and `StorageError`, and why does the distinction matter.
4. If the file could not be written, how could you recover without losing the order data.
5. What would happen if `process_orders` did not catch exceptions at all.

---

## Hints (from the end of the PDF)

- **For the first task**, write the validator first and test it in isolation before using it in the business logic. If the validator works, the business logic becomes simple.
- **For the second**, make sure that a failure in one order does not stop the entire batch. The summary should always be returned, even if every order fails.
- **Throughout the lab**, read the error messages carefully. They usually tell you exactly what is wrong. If you are stuck, print the values before the line that fails. Debugging is a skill, and this lab is designed to build it.
