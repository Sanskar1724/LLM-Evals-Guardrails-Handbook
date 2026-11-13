"""
Chapter 6 (optional) - The same check with Pydantic.

Pydantic is a popular free Python library for checking data.
You describe the shape of the data as a class, and Pydantic checks it.

This is the ONLY example in the handbook that needs an install:

    pip install pydantic

Run:  python ch06_structured_output_pydantic.py

No key needed.
"""

import sys

try:
    from typing import Literal

    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("Pydantic is not installed. Run:  pip install pydantic")
    print("(The file ch06_structured_output.py does the same job with no install.)")
    sys.exit(0)


class Ticket(BaseModel):
    # extra="forbid": reject fields we did not ask for.
    model_config = {"extra": "forbid"}

    category: Literal["billing", "delivery", "account", "other"]
    priority: int = Field(ge=1, le=5)            # ge = greater or equal, le = less or equal
    summary: str = Field(max_length=80)
    needs_human: bool


REPLIES = [
    '{"category": "billing", "priority": 4, "summary": "Charged twice.", "needs_human": true}',
    '{"category": "payments", "priority": 9, "summary": "Charged twice.", "needs_human": true}',
    '{"category": "billing", "priority": 2}',
    'not json at all',
]


def main():
    for reply in REPLIES:
        print("REPLY:", reply)
        try:
            ticket = Ticket.model_validate_json(reply)
            print("  valid ->", ticket)
        except ValidationError as error:
            for problem in error.errors():
                location = ".".join(str(part) for part in problem["loc"]) or "(whole reply)"
                print(f"  rejected -> {location}: {problem['msg']}")
        print()


if __name__ == "__main__":
    main()
