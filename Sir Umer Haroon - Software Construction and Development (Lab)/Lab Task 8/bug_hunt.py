"""SCD Lab Task 8, Task 2. Run: python bug_hunt.py."""

from crash_gallery import is_number


ORIGINAL_SOURCE = '''def calculate_discount(price, discount_percent):
    return price - price * discount_percent / 100

def calculate_average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / len(marks)

def find_student(students, name):
    for student in students:
        if student["name"] == name:
            return student
    return students[0]

def is_adult(age):
    if age > 18:
        return True
    else:
        return False

def apply_tax(amount, tax_rate):
    return amount + amount * tax_rate

def count_passed(marks, passing_mark=50):
    count = 0
    for mark in marks:
        if mark > passing_mark:
            count = count + 1
    return count
'''

original = {}
exec(ORIGINAL_SOURCE, original)


def calculate_discount(price, discount_percent):
    # Bug: invalid prices and discounts produced plausible but wrong totals.
    # Fix: validate types, nonnegative price, and the inclusive 0..100 range.
    if not is_number(price) or not is_number(discount_percent):
        return "Error: price and discount must be finite numbers"
    if price < 0:
        return "Error: price cannot be negative"
    if not 0 <= discount_percent <= 100:
        return "Error: discount must be between 0 and 100"
    return price - price * discount_percent / 100


def calculate_average(marks):
    # Bug: empty lists crashed; invalid marks were accepted or broke addition.
    # Fix: require a nonempty list of finite marks in the inclusive 0..100 range.
    if not isinstance(marks, list):
        return "Error: marks must be a list"
    if not marks:
        return "Error: cannot average empty list"
    if any(not is_number(mark) or not 0 <= mark <= 100 for mark in marks):
        return "Error: marks must be numbers between 0 and 100"
    return sum(marks) / len(marks)


def find_student(students, name):
    # Bug: an unsuccessful search returned the first student (or crashed).
    # Fix: validate records and explicitly return None when no name matches.
    if not isinstance(students, list) or not isinstance(name, str) or not name.strip():
        return "Error: provide a student list and a nonempty name"
    if any(not isinstance(student, dict) or not isinstance(student.get("name"), str)
           or not student["name"].strip() for student in students):
        return "Error: every student must have a nonempty text name"
    for student in students:
        if student["name"] == name:
            return student
    return None


def is_adult(age):
    # Bug: > 18 incorrectly excluded people who are exactly 18 years old.
    # Fix: reject invalid ages and use the inclusive >= 18 threshold.
    if type(age) is not int or age < 0:
        return False
    return age >= 18


def apply_tax(amount, tax_rate):
    # Bug: negative tax rates silently reduced the amount.
    # Fix: require finite, nonnegative amount and rate; rate is a fraction.
    if not is_number(amount) or not is_number(tax_rate):
        return "Error: amount and tax rate must be finite numbers"
    if amount < 0:
        return "Error: amount cannot be negative"
    if tax_rate < 0:
        return "Error: tax rate cannot be negative"
    return amount + amount * tax_rate


def count_passed(marks, passing_mark=50):
    # Bug: > passing_mark excluded scores exactly equal to the pass mark.
    # Fix: validate scores and threshold, then count with >= passing_mark.
    if not isinstance(marks, list):
        return "Error: marks must be a list"
    if not is_number(passing_mark) or not 0 <= passing_mark <= 100:
        return "Error: passing mark must be between 0 and 100"
    if any(not is_number(mark) or not 0 <= mark <= 100 for mark in marks):
        return "Error: marks must be numbers between 0 and 100"
    return sum(1 for mark in marks if mark >= passing_mark)


def collect_results():
    students = [{"name": "Ali", "age": 20}, {"name": "Sara", "age": 19}]
    cases = [
        ("calculate_discount", (100, 0), 100.0),
        ("calculate_discount", (100, 150), "Error: discount must be between 0 and 100"),
        ("calculate_discount", (100, 100), 0.0),
        ("calculate_discount", (100, -10), "Error: discount must be between 0 and 100"),
        ("calculate_discount", (-100, 10), "Error: price cannot be negative"),
        ("calculate_discount", (200, 25), 150.0),
        ("calculate_average", ([],), "Error: cannot average empty list"),
        ("calculate_average", ([0, 100],), 50.0),
        ("calculate_average", ([80, 90, 100],), 90.0),
        ("calculate_average", ([-10, 90],), "Error: marks must be numbers between 0 and 100"),
        ("calculate_average", ([101],), "Error: marks must be numbers between 0 and 100"),
        ("find_student", (students, "missing"), None),
        ("find_student", ([], "Ali"), None),
        ("find_student", (students, "Sara"), students[1]),
        ("find_student", ([{}], "Ali"), "Error: every student must have a nonempty text name"),
        ("is_adult", (18,), True),
        ("is_adult", (17,), False),
        ("is_adult", (19,), True),
        ("is_adult", (-1,), False),
        ("is_adult", ("18",), False),
        ("apply_tax", (100, -0.1), "Error: tax rate cannot be negative"),
        ("apply_tax", (100, 0), 100),
        ("apply_tax", (100, 0.1), 110.0),
        ("apply_tax", (-100, 0.1), "Error: amount cannot be negative"),
        ("apply_tax", (0, 0.1), 0.0),
        ("count_passed", ([50, 50, 50],), 3),
        ("count_passed", ([49, 50, 51],), 2),
        ("count_passed", ([],), 0),
        ("count_passed", ([59, 60, 61], 60), 2),
        ("count_passed", ([-1, 50],), "Error: marks must be numbers between 0 and 100"),
        ("count_passed", ([50], 101), "Error: passing mark must be between 0 and 100"),
    ]
    rows = []
    for name, args, expected in cases:
        try:
            value = original[name](*args)
            before = repr(value)
            bug = value != expected
        except Exception as error:
            before = type(error).__name__ + ": " + str(error)
            bug = True
        actual = globals()[name](*args)
        assert actual == expected, (name, args, actual, expected)
        display_args = ["students" if arg is students else repr(arg) for arg in args]
        rows.append(dict(function=name, call=name + "(" + ", ".join(display_args) + ")",
                         expected=repr(expected), original=before, bug=bug,
                         patched=repr(actual), passed=True))
    return rows


if __name__ == "__main__":
    results = collect_results()
    for row in results:
        print(row["call"])
        print("  Expected:", row["expected"])
        print("  Original:", row["original"], "Bug:", row["bug"])
        print("  Fixed:   ", row["patched"], "[PASS]")
    print(f"\n{len(results)}/{len(results)} fixed checks passed.")
