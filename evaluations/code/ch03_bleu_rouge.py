"""
Chapter 3 - BLEU and ROUGE written from scratch.

Run:  python ch03_bleu_rouge.py

These are small teaching versions. For real work use a tested library
(for example "sacrebleu" or "rouge-score"), because small details such as
tokenising and smoothing change the numbers.

No key needed. Standard library only.
"""

import math
from collections import Counter


def ngrams(tokens, n):
    """All groups of n words in order. ngrams([a,b,c], 2) -> [(a,b), (b,c)]"""
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def modified_precision(candidate, reference, n):
    """
    BLEU's n-gram precision with "clipping".
    Clipping: a word group in the candidate only counts as many times
    as it appears in the reference.
    Returns (matches, total).
    """
    cand_counts = Counter(ngrams(candidate, n))
    ref_counts = Counter(ngrams(reference, n))
    matches = sum(min(count, ref_counts[gram]) for gram, count in cand_counts.items())
    total = sum(cand_counts.values())
    return matches, total


def bleu(candidate, reference, max_n=4, smooth=False):
    """
    Sentence BLEU with one reference.
    smooth=True adds 1 to matches and totals for n > 1, so one missing
    4-gram does not turn the whole score into zero.
    """
    log_sum = 0.0
    for n in range(1, max_n + 1):
        matches, total = modified_precision(candidate, reference, n)
        if smooth and n > 1:
            matches, total = matches + 1, total + 1
        if matches == 0 or total == 0:
            return 0.0
        log_sum += math.log(matches / total)
    geometric_mean = math.exp(log_sum / max_n)

    # Brevity penalty: punish a candidate that is shorter than the reference.
    c, r = len(candidate), len(reference)
    brevity_penalty = 1.0 if c >= r else math.exp(1 - r / c)
    return brevity_penalty * geometric_mean


def rouge_n(candidate, reference, n):
    """ROUGE-N. Returns (precision, recall, f1) for n-gram overlap."""
    cand_counts = Counter(ngrams(candidate, n))
    ref_counts = Counter(ngrams(reference, n))
    overlap = sum(min(count, ref_counts[gram]) for gram, count in cand_counts.items())
    precision = overlap / max(1, sum(cand_counts.values()))
    recall = overlap / max(1, sum(ref_counts.values()))
    f1 = 0.0 if overlap == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def lcs_length(a, b):
    """Length of the longest common subsequence (words in the same order, gaps allowed)."""
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, word_a in enumerate(a, start=1):
        for j, word_b in enumerate(b, start=1):
            if word_a == word_b:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[len(a)][len(b)]


def rouge_l(candidate, reference):
    """ROUGE-L. Returns (precision, recall, f1) based on the LCS."""
    lcs = lcs_length(candidate, reference)
    precision = lcs / max(1, len(candidate))
    recall = lcs / max(1, len(reference))
    f1 = 0.0 if lcs == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def show(title, candidate_text, reference_text):
    candidate = candidate_text.lower().split()
    reference = reference_text.lower().split()
    print(title)
    print("  reference :", reference_text)
    print("  candidate :", candidate_text)
    for n in range(1, 5):
        matches, total = modified_precision(candidate, reference, n)
        print(f"  {n}-gram precision = {matches}/{total}")
    print(f"  BLEU-2            = {bleu(candidate, reference, max_n=2):.3f}")
    print(f"  BLEU-4            = {bleu(candidate, reference, max_n=4):.3f}")
    print(f"  BLEU-4 (smoothed) = {bleu(candidate, reference, max_n=4, smooth=True):.3f}")
    p, r, f = rouge_n(candidate, reference, 1)
    print(f"  ROUGE-1  P={p:.3f} R={r:.3f} F1={f:.3f}")
    p, r, f = rouge_n(candidate, reference, 2)
    print(f"  ROUGE-2  P={p:.3f} R={r:.3f} F1={f:.3f}")
    p, r, f = rouge_l(candidate, reference)
    print(f"  ROUGE-L  P={p:.3f} R={r:.3f} F1={f:.3f}")
    print()


def main():
    # Example 1: the worked example from the chapter.
    show("Example 1 - one word is different",
         "the cat sat on the mat",
         "the cat is on the mat")

    # Example 2: same meaning, different words. Word-overlap metrics give a low score.
    show("Example 2 - same meaning, different words",
         "a feline rests on the rug",
         "the cat is on the mat")

    # Example 3: a short candidate. Precision is perfect, the brevity penalty lowers BLEU.
    show("Example 3 - candidate is too short",
         "the cat",
         "the cat is on the mat")


if __name__ == "__main__":
    main()
