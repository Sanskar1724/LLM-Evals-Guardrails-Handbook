"""
Chapter 6 - Checking structured output (JSON) and asking again when it is wrong.

Run:  python ch06_structured_output.py

Apps often need the model to answer as JSON so that code can read it.
Models sometimes return broken JSON, miss a field, or invent a value.

This guard:
  1. pulls the JSON out of the reply (models like to wrap it in ``` fences)
  2. checks it against a small schema (required fields, types, allowed values, ranges)
  3. if it is wrong, sends the error back to the model and asks again ("re-ask")
  4. after too many tries, returns a safe default instead of crashing

The mock model fails twice before it gets it right, so you can watch the loop.

No key needed. Standard library only.
(A version that uses the popular Pydantic library is in ch06_structured_output_pydantic.py)
"""

import json
import re

# A small schema for a support ticket.
SCHEMA = {
    "category": {"type": str, "allowed": ["billing", "delivery", "account", "other"]},
    "priority": {"type": int, "min": 1, "max": 5},
    "summary": {"type": str, "max_length": 80},
    "needs_human": {"type": bool},
}

SAFE_DEFAULT = {"category": "other", "priority": 3, "summary": "Could not read ticket.", "needs_human": True}


def extract_json(text):
    """Find the first {...} block. Handles ```json fences and extra words around it."""
    text = re.sub(r"```(?:json)?", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found in the reply")
    return json.loads(text[start:end + 1])      # may raise json.JSONDecodeError (a ValueError)


def validate(data, schema):
    """Returns a list of error messages. Empty list = valid."""
    errors = []
    if not isinstance(data, dict):
        return ["the reply must be a JSON object"]
    for field, rule in schema.items():
        if field not in data:
            errors.append(f"missing field '{field}'")
            continue
        value = data[field]
        expected = rule["type"]
        # In Python, True is also an int. We do not accept a bool where a number is needed.
        wrong_type = not isinstance(value, expected) or (expected is int and isinstance(value, bool))
        if wrong_type:
            errors.append(f"'{field}' must be {expected.__name__}, got {type(value).__name__}")
            continue
        if "allowed" in rule and value not in rule["allowed"]:
            errors.append(f"'{field}' must be one of {rule['allowed']}, got '{value}'")
        if "min" in rule and value < rule["min"]:
            errors.append(f"'{field}' must be at least {rule['min']}")
        if "max" in rule and value > rule["max"]:
            errors.append(f"'{field}' must be at most {rule['max']}")
        if "max_length" in rule and len(value) > rule["max_length"]:
            errors.append(f"'{field}' must be at most {rule['max_length']} characters")
    for field in data:
        if field not in schema:
            errors.append(f"unknown field '{field}'")
    return errors


class MockModel:
    """Fails in two different ways, then answers correctly."""

    def __init__(self):
        self.calls = 0

    def __call__(self, prompt):
        self.calls += 1
        if self.calls == 1:
            # broken JSON: a trailing comma, wrapped in a code fence
            return 'Sure! Here it is:\n```json\n{"category": "billing", "priority": 2,}\n```'
        if self.calls == 2:
            # valid JSON, but wrong values
            return '{"category": "payments", "priority": "high", "summary": "Charged twice", "needs_human": true}'
        return '{"category": "billing", "priority": 4, "summary": "Customer was charged twice for one order.", "needs_human": true}'


def get_structured(model, user_text, max_tries=3):
    prompt = (
        "Read the support message and reply with JSON only.\n"
        "Fields: category (billing/delivery/account/other), priority (1-5), "
        "summary (max 80 characters), needs_human (true/false).\n"
        "Message: " + user_text
    )
    for attempt in range(1, max_tries + 1):
        reply = model(prompt)
        try:
            data = extract_json(reply)
            errors = validate(data, SCHEMA)
        except ValueError as error:
            data, errors = None, [f"invalid JSON: {error}"]

        if not errors:
            print(f"  try {attempt}: valid")
            return data, attempt
        print(f"  try {attempt}: rejected -> {'; '.join(errors)}")
        # Re-ask: tell the model exactly what was wrong.
        prompt += "\n\nYour last reply was rejected: " + "; ".join(errors) + "\nReply again with correct JSON only."

    print("  giving up -> using the safe default")
    return dict(SAFE_DEFAULT), max_tries


def main():
    print("Case 1: the model fixes itself after two re-asks")
    data, tries = get_structured(MockModel(), "I was charged two times for my order!")
    print("  result:", data)

    print()
    print("Case 2: the model never gets it right")
    data, tries = get_structured(lambda prompt: "I think this is about billing.", "I was charged two times!")
    print("  result:", data)


if __name__ == "__main__":
    main()
