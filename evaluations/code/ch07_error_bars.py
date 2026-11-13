"""
Chapter 7 - How sure can you be about a score? (error bars)

Run:  python ch07_error_bars.py

An eval score comes from a limited number of questions.
With other questions the score would be a bit different.
A "confidence interval" shows that range.

Part 1: the interval gets smaller when the test set gets bigger.
Part 2: the same thing with the bootstrap (resampling) method.
Part 3: comparing two models on the SAME questions.

No key needed. Standard library only.
"""

import math
import random


def interval_for_pass_rate(passes, total):
    """95% confidence interval for a pass rate (normal approximation)."""
    rate = passes / total
    standard_error = math.sqrt(rate * (1 - rate) / total)
    low = max(0.0, rate - 1.96 * standard_error)
    high = min(1.0, rate + 1.96 * standard_error)
    return rate, low, high


def bootstrap_interval(scores, rounds=2000, seed=0):
    """
    Bootstrap: draw a new test set of the same size from the old one
    (with repeats), many times, and look at how the average moves.
    """
    rng = random.Random(seed)
    n = len(scores)
    averages = []
    for _ in range(rounds):
        sample = [scores[rng.randrange(n)] for _ in range(n)]
        averages.append(sum(sample) / n)
    averages.sort()
    return averages[int(0.025 * rounds)], averages[int(0.975 * rounds)]


def main():
    print("PART 1 - same 80% score, different test set sizes")
    for total in (20, 100, 500, 2000):
        passes = int(0.8 * total)
        rate, low, high = interval_for_pass_rate(passes, total)
        print(f"  {passes:4}/{total:<4} = {rate:.0%}   95% interval: {low:.1%} to {high:.1%}")
    print("  With 20 questions, '80%' could really be anywhere from about 62% to 98%.")

    print()
    print("PART 2 - bootstrap on 50 results")
    rng = random.Random(1)
    scores_a = [1 if rng.random() < 0.80 else 0 for _ in range(50)]
    low, high = bootstrap_interval(scores_a)
    print(f"  model A passed {sum(scores_a)}/50 = {sum(scores_a)/50:.0%}")
    print(f"  bootstrap 95% interval: {low:.0%} to {high:.0%}")

    print()
    print("PART 3 - is model B really better than model A?")
    # Model B gets right everything A gets right, plus some of the hard ones.
    scores_b = [1 if a == 1 or rng.random() < 0.35 else 0 for a in scores_a]
    differences = [b - a for a, b in zip(scores_a, scores_b)]   # paired: same question
    mean_difference = sum(differences) / len(differences)
    low, high = bootstrap_interval(differences)
    print(f"  model B passed {sum(scores_b)}/50 = {sum(scores_b)/50:.0%}")
    print(f"  average difference (B - A) = {mean_difference:+.0%}")
    print(f"  bootstrap 95% interval for the difference: {low:+.0%} to {high:+.0%}")
    if low > 0:
        print("  The interval is fully above 0, so B is very likely better on this kind of question.")
    else:
        print("  The interval includes 0, so we cannot say B is better yet. Add more questions.")


if __name__ == "__main__":
    main()
