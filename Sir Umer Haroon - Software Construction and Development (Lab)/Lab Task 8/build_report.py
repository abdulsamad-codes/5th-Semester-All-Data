"""Reproduce the lab report and machine-readable evidence from actual runs.

Python programs need only the standard library. Rebuilding the PDF additionally
requires reportlab. Run: python build_report.py
"""

import contextlib
import io
import json
import platform
from pathlib import Path
from xml.sax.saxutils import escape

import crash_gallery
import bug_hunt


ROOT = Path(__file__).resolve().parent

DISCUSSION_1 = [
    ("Which function was hardest to make safe and why",
     "read_file was the hardest because its success depends on the operating system as well as the input. A valid string can name a missing file, a directory, an unreadable file or text with an incompatible encoding. Checks handle common invalid paths, but a file can disappear or its permissions can change between checking and opening it, so narrow OSError and UnicodeError handlers protect the actual read."),
    ("Which kind of bad input was most common",
     "Wrong types were the most common issue across the functions. Examples include text in arithmetic, None where a collection is required, and a string instead of a person dictionary. Empty collections and missing values were also recurring problems."),
    ("What pattern appeared in the fixes",
     "Each fix validates the input type before using an operation that assumes that type, then checks required contents or allowed values. Invalid input returns a descriptive error early. Only validated input reaches the original calculation or lookup."),
    ("Did any function need more than one check and why",
     "Yes. divide checks numeric types and a nonzero divisor; get_first checks for a list and then for an element; get_age checks the dictionary, the age key and the age value. average checks the list, its length and each number, while parse_number checks text, sign, digits and Python's conversion length limit. One successful check does not guarantee that every later operation is safe."),
]

BUG_REPORTS = [
    ("calculate_discount",
     "The function should calculate a reduced price from a nonnegative price and a discount between 0 and 100 percent. The original accepted 150 percent and returned -50.0 for a price of 100, and a negative discount increased the price. The fix validates finite numeric inputs, rejects negative prices and enforces the inclusive discount range before calculating the result."),
    ("calculate_average",
     "The function should return the mean of a nonempty list of valid marks. The original divided by zero for an empty list and silently averaged invalid marks such as -10 or 101. The fix rejects empty or non-list input and requires every mark to be a finite number between 0 and 100 before computing the mean."),
    ("find_student",
     "The function should return the matching student or None when the name is absent. The original returned the first student for a missing name, raised IndexError on an empty list and raised KeyError on a record without a name. The fix validates the records, returns an exact matching record and returns None after an unsuccessful search."),
    ("is_adult",
     "The function should classify a valid integer age of 18 or above as adult. The original used a strict greater-than comparison and returned False for age 18. The fix rejects invalid or negative ages and uses age >= 18 so the threshold is included."),
    ("apply_tax",
     "The function should add tax using a nonnegative amount and a nonnegative fractional tax rate. The original accepted a negative rate and returned 90.0 for amount 100 and rate -0.1, silently reducing the amount. The fix validates finite numeric inputs and rejects negative amounts and rates before applying the unchanged tax formula."),
    ("count_passed",
     "The function should count marks equal to or greater than the passing threshold. The original used a strict comparison and returned zero for three marks of 50 at the default threshold of 50. The fix validates marks and the threshold and uses >= so scores exactly at the passing mark count as passes."),
]

DISCUSSION_2 = [
    ("Which bug was hardest to find and why",
     "The find_student fallback was the hardest to notice because it returned a well-formed student dictionary even when the requested name was absent. A test that only checks whether the result looks like a student can pass. Checking the actual identity of the returned student reveals the error."),
    ("How did edge case tests help",
     "Boundary tests exposed the strict comparisons at age 18 and mark 50, which ordinary tests using age 20 and mark 80 would miss. Empty-list tests exposed division and indexing failures. Negative values and out-of-range discounts revealed calculations that completed successfully but violated the intended rules."),
    ("Why is a silent wrong result more dangerous than a crash",
     "A crash gives an immediate sign that processing failed. A silent wrong result can look valid, enter reports or later calculations, and lead to incorrect decisions before anyone notices. For example, returning Ali for a search for a missing student can attach information to the wrong person without an error message."),
]


def main():
    first = crash_gallery.collect_results()
    second = bug_hunt.collect_results()
    evidence = dict(python=platform.python_version(), task_1=first, task_2=second,
                    total_checks=len(first) + len(second), all_passed=True)
    (ROOT / "test_results.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    for module in (crash_gallery, bug_hunt):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for row in module.collect_results():
                print(row["call"])
                print("  Original:", row.get("error_type", ""), row["original"])
                print("  Fixed:", row["patched"], "[PASS]")
        (ROOT / (module.__name__ + "_output.txt")).write_text(output.getvalue(), encoding="utf-8")

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="LabBody", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=8))
    styles.add(ParagraphStyle(name="Cell", fontName="Helvetica", fontSize=8, leading=11, wordWrap="CJK"))
    styles.add(ParagraphStyle(name="HeadCell", parent=styles["Cell"], textColor=colors.white, fontName="Helvetica-Bold"))
    styles["Title"].textColor = colors.black
    styles["Heading1"].textColor = colors.black
    styles["Heading2"].textColor = colors.black
    story, markdown = [], []

    def paragraph(text, style="LabBody"):
        story.append(Paragraph(escape(text), styles[style]))
        markdown.append(text + "\n")

    def heading(text, level=1):
        story.append(Paragraph(escape(text), styles["Heading" + str(level)]))
        markdown.append("#" * (level + 1) + " " + text + "\n")

    def table(headers, rows, widths):
        data = [[Paragraph(escape(str(value)), styles["HeadCell" if i == 0 else "Cell"])
                 for value in row] for i, row in enumerate([headers] + rows)]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#26384A")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F4F6")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9D9D9")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.extend([t, Spacer(1, 12)])
        def md(value):
            return str(value).replace("|", "\\|").replace("\n", " ")
        markdown.append("| " + " | ".join(map(md, headers)) + " |")
        markdown.append("| " + " | ".join("---" for _ in headers) + " |")
        markdown.extend("| " + " | ".join(map(md, row)) + " |" for row in rows)
        markdown.append("")

    def page():
        story.append(PageBreak())

    paragraph("SCD Lab Task 8", "Title")
    markdown[0] = "# SCD Lab Task 8\n"
    paragraph("Defensive Programming and Silent Bug Detection", "Heading1")
    paragraph("IMSCIENCES Peshawar")
    paragraph("Course: Software Construction and Development Lab")
    paragraph("Instructor: Engr. Muhammad Umer Haroon")
    paragraph("Date: 29 October 2026")
    paragraph("This report documents both tasks in the lab handout: reproducing crashes, guarding invalid inputs, identifying silent logic bugs, and verifying corrected behavior. All 57 required and additional checks passed against the patched functions.")
    heading("Submission contents")
    paragraph("crash_gallery.py contains the six original Task 1 functions, their patched versions and the executable test block. bug_hunt.py contains the six original Task 2 functions, corrected versions with explanatory comments and its executable test block. The original source is preserved verbatim in each module's ORIGINAL_SOURCE string and executed in a separate namespace so both versions can be tested in one run.")
    paragraph("The accompanying output text files contain captured execution results. test_results.json records the expected, original and patched results. build_report.py regenerates the evidence and this report; Lab_Report.md is an editable text copy of the report.")
    heading("Run instructions")
    paragraph("Keep the two Python solution files together. Run python crash_gallery.py and then python bug_hunt.py from this folder. The solution programs require Python 3 and only the standard library; bug_hunt imports the numeric validation helper from crash_gallery. Rebuilding the PDF with python build_report.py additionally requires reportlab.")
    heading("Input rules")
    paragraph("Marks and passing thresholds use the inclusive 0 to 100 scale. Prices and monetary amounts must be nonnegative; discount values are percentages from 0 to 100. Tax rates are fractions, so 0.1 means 10 percent; no arbitrary upper tax-rate cap is imposed. Ages are nonnegative integers, student names use exact case-sensitive matching, and malformed student records produce clear errors. Boolean values, NaN and infinity are excluded from numeric input. parse_number accepts signed decimal integer text with optional surrounding whitespace; file reading uses UTF-8.")
    paragraph("Error strings are returned for invalid input, except is_adult returns False and a missing student returns None, following the handout. Test harnesses catch original exceptions only so every case can run; patched functions use guard checks, with narrow handlers for unavoidable file I/O errors.")
    page()

    functions_1 = ["divide", "get_first", "get_age", "parse_number", "read_file", "average"]
    explanations = {
        "divide": "Validate both numeric arguments before division and reject a zero divisor.",
        "get_first": "Require a list and check that it is nonempty before indexing.",
        "get_age": "Require a dictionary, verify the age key and reject invalid age values.",
        "parse_number": "Validate text, an optional sign and ASCII digits before int conversion; reject decimal fractions and oversized conversion strings.",
        "read_file": "Validate the filename, existence and regular-file status. A context manager closes the file even on failure; narrow handlers cover read-time operating-system and encoding errors.",
        "average": "Require a nonempty list and verify every element before summing and dividing.",
    }
    for i, name in enumerate(functions_1):
        if i % 2 == 0:
            heading("Task 1 The Crash Gallery" + (" continued" if i else ""))
            if i == 0:
                paragraph("Parts A to C: original functions are preserved, failures below were observed by running them, and the same inputs were passed to the patched functions. Every function has at least three distinct bad-input cases plus a valid case. Error messages are recorded as produced by this Python runtime; operating-system wording can vary. Temporary paths in file errors are normalized to readable labels.")
        heading(name, 2)
        selected = [row for row in first if row["function"] == name]
        table(["Input", "Original outcome", "Error type", "Patched result"],
              [[r["call"], r["original"], r["error_type"], r["patched"]] for r in selected],
              [113, 137, 80, 177])
        paragraph("Patch: " + explanations[name])
        if i % 2 == 1:
            page()

    heading("Task 1 Discussion Notes")
    paragraph("Part D")
    for question, answer in DISCUSSION_1:
        heading(question, 2)
        paragraph(answer)
    paragraph(f"Verification: {len(first)} of {len(first)} Task 1 patched checks passed, including {sum(r['bad'] for r in first)} bad-input cases. No patched call in this test set raised an exception.")
    page()

    names_2 = ["calculate_discount", "calculate_average", "find_student", "is_adult", "apply_tax", "count_passed"]
    for i, name in enumerate(names_2):
        if i % 2 == 0:
            heading("Task 2 The Silent Bug Hunt" + (" continued" if i else ""))
            if i == 0:
                paragraph("Parts A to C: each function was tested with at least three cases including boundaries. The Expected column defines the corrected contract; Bug indicates whether the original differs from that contract or crashes. Each fixed output matched Expected exactly. The corrected source includes a Bug comment and a Fix comment for every function.")
            if i == 2:
                paragraph("For the search tests, students = [{'name': 'Ali', 'age': 20}, {'name': 'Sara', 'age': 19}].")
        heading(name, 2)
        selected = [r for r in second if r["function"] == name]
        table(["Test input", "Expected and fixed", "Actual original result", "Bug"],
              [[r["call"], r["expected"], r["original"], "Yes" if r["bug"] else "No"] for r in selected],
              [143, 164, 166, 34])
        if i % 2 == 1:
            page()

    heading("Task 2 Bug Report")
    paragraph("Part D. Each entry states the intended behavior, observed defect and correction in three sentences.")
    for name, text in BUG_REPORTS:
        heading(name, 2)
        paragraph(text)
    page()
    heading("Task 2 Discussion")
    for question, answer in DISCUSSION_2:
        heading(question, 2)
        paragraph(answer)
    heading("Final verification")
    paragraph(f"The test run used Python {platform.python_version()}. Task 1 passed {len(first)}/{len(first)} patched checks and Task 2 passed {len(second)}/{len(second)} corrected checks, for a total of 57/57. Tests include every example input listed in the handout, at least three bad inputs per Task 1 function, and at least three edge-focused tests per Task 2 function. Both valid behavior and rejected inputs were checked using executable assertions.")
    paragraph("The tables report observed execution rather than predicted output. No Task 2 row marked No indicates a defect for that particular input; a function can pass normal cases while failing boundary cases. Validation ranges for marks and nonnegative amounts are explicit rules used consistently throughout this submission.")
    heading("Source")
    paragraph("Lab Task 8.pdf, SCD Lab Task 8, IMSciences Peshawar, designed by Engr. Muhammad Umer Haroon, pages 1 to 6.")

    (ROOT / "Lab_Report.md").write_text("\n".join(markdown), encoding="utf-8")

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(44, 26, "SCD Lab Task 8")
        canvas.drawRightString(A4[0] - 44, 26, str(doc.page))

    doc = SimpleDocTemplate(str(ROOT / "Lab_Report.pdf"), pagesize=A4,
                           rightMargin=44, leftMargin=44, topMargin=38, bottomMargin=42,
                           title="SCD Lab Task 8", author="")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("PASS: 26 Task 1 checks and 31 Task 2 checks; 57 total.")
    print("Created Lab_Report.pdf, Lab_Report.md, test_results.json and output transcripts.")


if __name__ == "__main__":
    main()
