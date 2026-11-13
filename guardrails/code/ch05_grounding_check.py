"""
Chapter 5 - A grounding check for hallucinations.

Run:  python ch05_grounding_check.py

"Grounded" means: every claim in the answer can be found in the source text.
A hallucination is a claim that sounds right but is not supported.

This guard:
  1. splits the answer into sentences
  2. checks each sentence against the source (shared words + exact numbers)
  3. removes sentences that are not supported, or refuses if too little is left

Real systems use an LLM or an NLI model for step 2.
(NLI = natural language inference: a model that says if text A supports text B.)
Word rules are a rough stand-in so the example runs anywhere.

No key needed. Standard library only.
"""

import re

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "of", "in", "on",
    "at", "for", "and", "or", "it", "its", "this", "that", "with", "as", "by",
    "from", "you", "your", "can", "will", "do", "does", "we", "our", "has", "have",
}


def content_words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP_WORDS}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def support_score(claim, source_sentences):
    """
    Best share of the claim's content words found in one source sentence.
    If the claim has a number that is not in that source sentence, the score is 0.
    """
    claim_words = content_words(claim)
    claim_numbers = set(re.findall(r"\d+(?:\.\d+)?", claim))
    if not claim_words:
        return 1.0
    best = 0.0
    for source in source_sentences:
        source_numbers = set(re.findall(r"\d+(?:\.\d+)?", source))
        if not claim_numbers <= source_numbers:
            continue
        share = len(claim_words & content_words(source)) / len(claim_words)
        best = max(best, share)
    return best


def grounding_guard(answer, source, threshold=0.6):
    """
    Returns (final_answer, report).
    report is a list of (sentence, score, kept).
    """
    source_sentences = sentences(source)
    report = []
    kept = []
    for claim in sentences(answer):
        score = support_score(claim, source_sentences)
        ok = score >= threshold
        report.append((claim, score, ok))
        if ok:
            kept.append(claim)

    if not kept:
        return "I could not find this in the documents I have.", report
    final = " ".join(kept)
    if len(kept) < len(report):
        final += " (Some parts were removed because I could not verify them.)"
    return final, report


def main():
    source = (
        "The college library opens at 8 am and closes at 9 pm on weekdays. "
        "On Sunday the library is closed. "
        "Students can borrow up to 4 books for 14 days. "
        "The late fee is 2 rupees per day for each book."
    )
    answers = {
        "grounded answer":
            "Students can borrow up to 4 books for 14 days. The late fee is 2 rupees per day for each book.",
        "one made-up claim":
            "Students can borrow up to 4 books for 14 days. The late fee is 10 rupees per day for each book. "
            "The library also has a free coffee machine on every floor.",
        "fully made up":
            "The library is open 24 hours and offers free laptops.",
    }
    print("SOURCE:", source)
    for name, answer in answers.items():
        final, report = grounding_guard(answer, source)
        print()
        print(f"--- {name} ---")
        for claim, score, ok in report:
            print(f"  [{'keep' if ok else 'DROP'}] support={score:.2f}  {claim}")
        print("  FINAL:", final)


if __name__ == "__main__":
    main()
