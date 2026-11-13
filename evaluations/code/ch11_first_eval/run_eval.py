"""
Chapter 11 - Build your first eval.

Run:  python run_eval.py

What it does:
  1. reads the test cases from dataset.jsonl
  2. asks the app each question
  3. grades each answer with simple code checks
  4. prints a report, grouped by tag
  5. saves all details to last_run.json so you can read the failures

With no key the app uses its mock bot (which has 2 bugs on purpose).
With a key it uses a real free model: 12 requests per run.
"""

import json
import os
import re

from app import answer_question

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_WORDS = 60     # the bot must keep answers short


def load_dataset(path):
    cases = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def contains(answer, phrase):
    """
    Case-insensitive search.
    A short number like "5" must match as a whole number, so "5" is not found inside "50".
    """
    if phrase.isdigit():
        return re.search(r"(?<!\d)" + re.escape(phrase) + r"(?!\d)", answer) is not None
    if phrase.isalpha() and len(phrase) <= 4:
        return re.search(r"\b" + re.escape(phrase) + r"\b", answer, re.IGNORECASE) is not None
    return phrase.lower() in answer.lower()


def grade(case, answer):
    """Returns (passed, list of reasons for failing)."""
    problems = []
    for phrase in case["must_include"]:
        if not contains(answer, phrase):
            problems.append(f"missing '{phrase}'")
    for phrase in case["must_not_include"]:
        if contains(answer, phrase):
            problems.append(f"has forbidden '{phrase}'")
    if len(answer.split()) > MAX_WORDS:
        problems.append(f"too long ({len(answer.split())} words)")
    return len(problems) == 0, problems


def main():
    cases = load_dataset(os.path.join(HERE, "dataset.jsonl"))
    results = []
    for case in cases:
        answer = answer_question(case["question"])
        passed, problems = grade(case, answer)
        results.append({**case, "answer": answer, "passed": passed, "problems": problems})

    print()
    print(f"{'id':20} {'tag':18} result")
    print("-" * 60)
    for r in results:
        line = f"{r['id']:20} {r['tag']:18} {'PASS' if r['passed'] else 'FAIL'}"
        if not r["passed"]:
            line += "  <- " + "; ".join(r["problems"])
        print(line)

    print()
    print("Pass rate by tag:")
    for tag in sorted({r["tag"] for r in results}):
        group = [r for r in results if r["tag"] == tag]
        passed = sum(r["passed"] for r in group)
        print(f"  {tag:18} {passed}/{len(group)}")

    total_passed = sum(r["passed"] for r in results)
    print()
    print(f"TOTAL: {total_passed}/{len(results)} = {total_passed / len(results):.0%}")

    print()
    print("Failures to read:")
    for r in results:
        if not r["passed"]:
            print(f"  Q: {r['question']}")
            print(f"  A: {r['answer']}")
            print(f"     problems: {', '.join(r['problems'])}")

    out_path = os.path.join(HERE, "last_run.json")
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)
    print()
    print("Saved details to last_run.json")


if __name__ == "__main__":
    main()
