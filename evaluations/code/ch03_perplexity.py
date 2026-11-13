"""
Chapter 3 - Perplexity.

Run:  python ch03_perplexity.py

Perplexity tells us how "surprised" a language model is by a text.
Low perplexity = the model found the text easy to predict.

Part 1: perplexity from a list of probabilities (the formula).
Part 2: a tiny bigram language model, trained on a few sentences.

No key needed. Standard library only.
"""

import math
from collections import Counter


def perplexity_from_probs(probabilities):
    """
    probabilities: the probability the model gave to each real next token.
    perplexity = exp( - average of log(p) )
    """
    average_log = sum(math.log(p) for p in probabilities) / len(probabilities)
    return math.exp(-average_log)


class BigramModel:
    """Predicts the next word from the one word before it."""

    def __init__(self, sentences):
        self.pair_counts = Counter()
        self.word_counts = Counter()
        self.vocabulary = set()
        for sentence in sentences:
            words = ["<s>"] + sentence.lower().split() + ["</s>"]
            self.vocabulary.update(words)
            for previous, current in zip(words, words[1:]):
                self.pair_counts[(previous, current)] += 1
                self.word_counts[previous] += 1

    def probability(self, previous, current):
        # Add-one smoothing: unseen pairs get a small probability, not zero.
        return (self.pair_counts[(previous, current)] + 1) / (
            self.word_counts[previous] + len(self.vocabulary)
        )

    def perplexity(self, sentence):
        words = ["<s>"] + sentence.lower().split() + ["</s>"]
        probs = [self.probability(p, c) for p, c in zip(words, words[1:])]
        return perplexity_from_probs(probs)


def main():
    print("PART 1 - the formula")
    probs = [0.5, 0.25, 0.5, 0.25]
    print("  token probabilities:", probs)
    print(f"  perplexity = {perplexity_from_probs(probs):.3f}")
    print("  Meaning: on average the model was as unsure as if it had to pick")
    print("  between about 2.8 equally likely words at each step.")
    print()
    print("  A model that is always sure and right:", f"{perplexity_from_probs([1.0, 1.0, 1.0]):.3f}")
    print("  A model that guesses among 10 words  :", f"{perplexity_from_probs([0.1, 0.1, 0.1]):.3f}")

    print()
    print("PART 2 - tiny bigram model")
    training = [
        "the cat sat on the mat",
        "the dog sat on the rug",
        "the cat ate the fish",
        "the dog ate the bone",
    ]
    model = BigramModel(training)
    for sentence in ["the cat sat on the rug", "the dog ate the fish", "rug the on sat cat the"]:
        print(f"  {sentence!r:28} perplexity = {model.perplexity(sentence):6.2f}")
    print("  The scrambled sentence has the highest perplexity: it surprises the model most.")


if __name__ == "__main__":
    main()
