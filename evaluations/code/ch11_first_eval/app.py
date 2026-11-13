"""
The app we want to test: a small FAQ bot for an online shop.

answer_question(question) -> str

With no key it uses a mock bot (keyword lookup).
With OPENROUTER_API_KEY set it asks a real free model, with the FAQ in the prompt.
"""

import os
import sys

# Let this file import llm_client.py from the folder above.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from llm_client import ask_llm  # noqa: E402

FAQ = """
- Refunds take 5 working days and go to the original payment method.
- Delivery costs 40 rupees. Orders above 500 rupees get free delivery.
- You can change the delivery address within 2 hours of ordering.
- Support is open from 9 am to 6 pm, Monday to Saturday.
- We deliver only inside India.
"""

SYSTEM_PROMPT = (
    "You are a support bot for an online shop. Answer in one or two short sentences. "
    "Use only the FAQ below. If the FAQ does not have the answer, say: "
    "'I do not know. Please contact support.' Never promise anything that is not in the FAQ.\n"
    "FAQ:\n" + FAQ
)


def mock_bot(question):
    """Keyword lookup. It has two bugs on purpose, so the eval has something to find."""
    q = question.lower()
    if "refund" in q:
        return "Refunds take 5 working days and go to the original payment method."
    if "free delivery" in q or "free shipping" in q:
        return "Orders above 500 rupees get free delivery."
    if "delivery" in q and ("cost" in q or "fee" in q or "charge" in q):
        return "Delivery costs 40 rupees."
    if "address" in q:
        # BUG 1: wrong number (the FAQ says 2 hours).
        return "You can change the delivery address within 24 hours of ordering."
    if "open" in q or "timing" in q or "hours" in q:
        return "Support is open from 9 am to 6 pm, Monday to Saturday."
    if "discount" in q or "coupon" in q:
        # BUG 2: makes up an offer that is not in the FAQ.
        return "Yes! Use code SAVE50 for 50 percent off."
    return "I do not know. Please contact support."


def answer_question(question):
    return ask_llm(question, system=SYSTEM_PROMPT, mock=mock_bot, max_tokens=120)


if __name__ == "__main__":
    for q in ["How long do refunds take?", "Do you sell cars?"]:
        print("Q:", q)
        print("A:", answer_question(q))
