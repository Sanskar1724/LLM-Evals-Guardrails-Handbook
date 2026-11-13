"""
Chapter 3 - Finding and hiding PII (personal data) with rules.

Run:  python ch03_pii_redaction.py

PII = personally identifiable information: data that points to a real person,
such as an email address, a phone number or a card number.

Steps:
  1. find PII with regular expressions (plus a checksum for card numbers)
  2. replace each item with a placeholder like <EMAIL_1>
  3. send the safe text to the model
  4. put the real values back in the answer if the user is allowed to see them

All the data below is fake.

Rules find PII with a fixed shape (emails, numbers). They do NOT find names
or addresses well. Tools like Presidio add a language model for those.

No key needed. Standard library only.
"""

import re


def luhn_ok(number_text):
    """
    Luhn checksum. Real card numbers pass it. Most random digit strings do not.
    This removes many false alarms (for example order numbers).
    """
    digits = [int(ch) for ch in number_text if ch.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    total = 0
    for position, digit in enumerate(reversed(digits)):
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


# Order matters: more specific patterns first.
PATTERNS = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"), None),
    ("CARD", re.compile(r"\b\d(?:[ -]?\d){12,18}\b"), luhn_ok),
    ("API_KEY", re.compile(r"\b(?:sk|pk|key)-[A-Za-z0-9_-]{16,}\b"), None),
    ("IP", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), None),
    ("PHONE", re.compile(r"(?<![\w.])(?:\+?\d{1,3}[ -]?)?\d{10}(?!\w)|(?<![\w.])\+?\d{1,3}[ -]\d{3,5}[ -]\d{5,7}(?!\w)"), None),
]


def redact(text):
    """
    Returns (safe_text, mapping).
    mapping lets us restore the real values later: {"<EMAIL_1>": "a@b.com", ...}
    """
    mapping = {}
    counters = {}

    for label, pattern, extra_check in PATTERNS:
        def replace(match, label=label, extra_check=extra_check):
            value = match.group(0)
            if extra_check and not extra_check(value):
                return value                      # looks similar but fails the check: keep it
            for placeholder, known in mapping.items():
                if known == value:
                    return placeholder            # same value -> same placeholder
            counters[label] = counters.get(label, 0) + 1
            placeholder = f"<{label}_{counters[label]}>"
            mapping[placeholder] = value
            return placeholder

        text = pattern.sub(replace, text)
    return text, mapping


def restore(text, mapping):
    """Put the real values back."""
    for placeholder, value in mapping.items():
        text = text.replace(placeholder, value)
    return text


def mock_model(prompt):
    """A fake model that writes a reply using whatever it was given."""
    email = re.search(r"<EMAIL_\d+>", prompt)
    target = email.group(0) if email else "your email"
    return f"Thanks. We will send the receipt to {target} today."


def main():
    message = (
        "Hi, I am Asha. My email is asha.k@example.com and my phone is +91 98765 43210. "
        "I paid with card 4111 1111 1111 1111 for order 1234567890123456. "
        "My test key is sk-test_abcdefghijklmnop1234 and I logged in from 192.168.1.20."
    )
    print("ORIGINAL:")
    print(" ", message)

    safe_text, mapping = redact(message)
    print()
    print("SENT TO THE MODEL:")
    print(" ", safe_text)
    print()
    print("MAPPING (kept on our side, never sent):")
    for placeholder, value in mapping.items():
        print(f"  {placeholder:12} -> {value}")

    answer = mock_model(safe_text)
    print()
    print("MODEL ANSWER  :", answer)
    print("AFTER RESTORE :", restore(answer, mapping))

    print()
    print("Notes:")
    print(" * The order number has 16 digits but fails the Luhn check, so it was NOT hidden as a card.")
    print(" * The name 'Asha' was NOT found. Rules cannot find names. That is a known limit.")


if __name__ == "__main__":
    main()
