"""
Chapter 4 - A simple content moderation filter.

Run:  python ch04_moderation_filter.py

Two layers:
  Layer 1: fast word rules with categories and severity (free, instant)
  Layer 2: a classifier for the unclear cases (here: a mock;
           with OPENROUTER_API_KEY set, a real free model is asked)

The word lists use mild words only. Real lists are longer and are kept private.

Uses up to 2 real requests when a key is set.
"""

import re

from llm_client import ask_llm

# category -> (severity, list of patterns)
# severity 2 = block at once, severity 1 = unclear, ask layer 2
WORD_RULES = {
    "threat": (2, [r"\bi will (hurt|kill|find) you\b", r"\byou will regret\b"]),
    "self_harm": (2, [r"\b(hurt|kill) myself\b", r"\bend my life\b"]),
    "insult": (1, [r"\b(idiot|stupid|moron|loser)\b"]),
    "violence_word": (1, [r"\b(kill|attack|destroy)\b"]),
}

# Safe phrases that contain a risky word. Checked first.
ALLOW_PHRASES = [
    r"\bkill (the|a|this|that) (process|task|job|server|app)\b",
    r"\bkilling time\b",
    r"\bheart attack\b",
]

SELF_HARM_MESSAGE = (
    "I am really sorry you feel this way. You are not alone. "
    "Please talk to someone you trust or contact a local helpline right now."
)


def layer1(text):
    """Returns (severity, categories). severity 0 = nothing found."""
    lower = text.lower()
    for phrase in ALLOW_PHRASES:
        lower = re.sub(phrase, " ", lower)       # remove known-safe phrases first
    worst = 0
    found = []
    for category, (severity, patterns) in WORD_RULES.items():
        if any(re.search(p, lower) for p in patterns):
            found.append(category)
            worst = max(worst, severity)
    return worst, found


def mock_classifier(prompt):
    """
    Fake layer-2 classifier.
    Rule: an insult aimed at a person ("you", "he", "she", "they") is unsafe.
    """
    text = prompt.split("TEXT:", 1)[1].lower()
    aimed_at_person = re.search(r"\b(you|he|she|they|u)\b.{0,20}\b(idiot|stupid|moron|loser)\b", text) \
        or re.search(r"\b(kill|attack|destroy)\b.{0,15}\b(you|him|her|them)\b", text)
    return "UNSAFE" if aimed_at_person else "SAFE"


def layer2(text):
    prompt = (
        "You are a content moderator. Reply with one word: SAFE or UNSAFE.\n"
        "UNSAFE means the text insults, threatens or harasses a person.\n"
        "Talking about a topic, or being hard on oneself, is SAFE.\n"
        "TEXT: " + text
    )
    reply = ask_llm(prompt, mock=mock_classifier, max_tokens=5).upper()
    return "UNSAFE" if "UNSAFE" in reply else "SAFE"


def moderate(text):
    """Returns (action, detail). action is allow / block / support."""
    severity, categories = layer1(text)
    if severity == 0:
        return "allow", "layer 1: nothing found"
    if "self_harm" in categories:
        return "support", "layer 1: self-harm -> show a caring message, do not just block"
    if severity == 2:
        return "block", "layer 1: " + ", ".join(categories)
    verdict = layer2(text)
    if verdict == "UNSAFE":
        return "block", "layer 2 said UNSAFE (" + ", ".join(categories) + ")"
    return "allow", "layer 2 said SAFE (" + ", ".join(categories) + ")"


EXAMPLES = [
    "How do I bake bread?",
    "How do I kill a process on Linux?",
    "My grandfather had a heart attack last year.",
    "You are such an idiot.",
    "I felt stupid when I forgot my keys.",
    "I will find you and you will regret this.",
    "Sometimes I want to end my life.",
    "The class passed the assessment.",        # contains 'ass' inside words: must not trigger
]


def main():
    for text in EXAMPLES:
        action, detail = moderate(text)
        print(f"[{action:7}] {text}")
        print(f"          {detail}")
        if action == "support":
            print(f"          reply: {SELF_HARM_MESSAGE}")
    print()
    print("Things to notice:")
    print(" * Word boundaries (\\b) stop matches inside other words ('class', 'assessment').")
    print(" * The allow list fixes 'kill a process' and 'heart attack'.")
    print(" * Layer 2 tells 'You are an idiot' from 'I felt stupid'.")
    print(" * Self-harm text gets a caring reply, not a cold block.")


if __name__ == "__main__":
    main()
