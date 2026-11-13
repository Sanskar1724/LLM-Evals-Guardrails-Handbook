"""
Chapter 3 - The idea behind BERTScore, with toy numbers.

Run:  python ch03_bertscore_idea.py

Real BERTScore uses a BERT model to turn every token into a vector
(a list of numbers that holds meaning). That needs a large download.

Here we use tiny hand-made vectors so you can see the method:
  1. turn each word into a vector
  2. compare every candidate word with every reference word (cosine similarity)
  3. each word takes its best match ("greedy matching")
  4. average the best matches -> precision, recall, F1

The vectors below are invented for teaching. They are not from a real model.

No key needed. Standard library only.
"""

import math

# Toy 3-number vectors. Words with a similar meaning get similar numbers.
#            [animal, place/thing, action/other]
VECTORS = {
    "cat":    [0.95, 0.10, 0.05],
    "feline": [0.90, 0.15, 0.10],
    "dog":    [0.60, 0.05, 0.65],
    "mat":    [0.05, 0.95, 0.10],
    "rug":    [0.10, 0.90, 0.15],
    "sits":   [0.10, 0.20, 0.95],
    "rests":  [0.15, 0.25, 0.90],
    "runs":   [0.55, 0.02, 0.45],
    "on":     [0.33, 0.33, 0.33],
    "the":    [0.30, 0.35, 0.30],
    "a":      [0.32, 0.33, 0.31],
}


def cosine(u, v):
    """Cosine similarity: 1.0 = same direction, 0 = unrelated."""
    dot = sum(a * b for a, b in zip(u, v))
    length_u = math.sqrt(sum(a * a for a in u))
    length_v = math.sqrt(sum(b * b for b in v))
    return dot / (length_u * length_v)


def toy_bertscore(candidate_text, reference_text):
    candidate = candidate_text.lower().split()
    reference = reference_text.lower().split()

    # Precision: each candidate word finds its best match in the reference.
    precision = sum(
        max(cosine(VECTORS[c], VECTORS[r]) for r in reference) for c in candidate
    ) / len(candidate)

    # Recall: each reference word finds its best match in the candidate.
    recall = sum(
        max(cosine(VECTORS[r], VECTORS[c]) for c in candidate) for r in reference
    ) / len(reference)

    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def exact_word_overlap(candidate_text, reference_text):
    """Share of candidate words that also appear in the reference (like unigram precision)."""
    candidate = candidate_text.lower().split()
    reference = reference_text.lower().split()
    return sum(1 for word in candidate if word in reference) / len(candidate)


def main():
    reference = "the cat sits on the mat"
    candidates = [
        "the cat sits on the mat",      # identical
        "a feline rests on the rug",    # same meaning, new words
        "the dog runs on the mat",      # similar words, different meaning
    ]
    print("reference:", reference)
    print()
    for candidate in candidates:
        p, r, f = toy_bertscore(candidate, reference)
        overlap = exact_word_overlap(candidate, reference)
        print(f"candidate: {candidate}")
        print(f"  exact word overlap = {overlap:.2f}")
        print(f"  toy BERTScore      P={p:.3f} R={r:.3f} F1={f:.3f}")
        print()
    print("Look at candidate 2: almost no exact words match, but the vector score is high,")
    print("because 'feline' is close to 'cat' and 'rug' is close to 'mat'.")
    print("Look at candidate 3: the score is still quite high even though the meaning changed.")
    print("So embedding metrics are better than word overlap, but they are not perfect.")


if __name__ == "__main__":
    main()
