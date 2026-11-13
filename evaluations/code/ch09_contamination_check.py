"""
Chapter 9 - Seeing benchmark contamination with a toy model.

Run:  python ch09_contamination_check.py

"Contamination" means the test questions were in the model's training data.
The model can then score high by memory, without real skill.

One way to check: change the questions a little (new numbers, new wording)
and see if the score drops. Real skill should survive small changes.

Model 1 below only memorised the public test set.
Model 2 really does the sums.

No key needed. Standard library only.
"""

import re

# The "public benchmark". Imagine it was posted on the internet years ago.
PUBLIC_TEST = [
    ("Ravi has 3 apples and buys 4 more. How many apples does Ravi have?", 7),
    ("A book costs 20 rupees. How much do 5 books cost?", 100),
    ("There are 12 birds. 5 fly away. How many birds are left?", 7),
    ("A bus has 30 seats and 18 are taken. How many seats are free?", 12),
]

# The same kind of question with new names and new numbers.
FRESH_TEST = [
    ("Meena has 6 apples and buys 9 more. How many apples does Meena have?", 15),
    ("A pen costs 15 rupees. How much do 4 pens cost?", 60),
    ("There are 20 birds. 8 fly away. How many birds are left?", 12),
    ("A hall has 50 seats and 21 are taken. How many seats are free?", 29),
]


def memorising_model(question):
    """Knows the public test by heart. Guesses 0 for anything else."""
    memory = dict(PUBLIC_TEST)
    return memory.get(question, 0)


def reasoning_model(question):
    """Reads the numbers and picks the operation from simple word clues."""
    a, b = [int(n) for n in re.findall(r"\d+", question)][:2]
    text = question.lower()
    if "more" in text:
        return a + b
    if "cost" in text:
        return a * b
    return a - b      # "fly away", "taken"


def accuracy(model, test_set):
    return sum(model(question) == answer for question, answer in test_set) / len(test_set)


def main():
    print(f"{'model':18} {'public test':>12} {'fresh test':>11} {'drop':>6}")
    for name, model in [("memorising model", memorising_model), ("reasoning model", reasoning_model)]:
        public = accuracy(model, PUBLIC_TEST)
        fresh = accuracy(model, FRESH_TEST)
        print(f"{name:18} {public:>12.0%} {fresh:>11.0%} {public - fresh:>6.0%}")
    print()
    print("Both models get 100% on the public test.")
    print("Only the fresh test shows which one has real skill.")
    print("A big drop on changed questions is a warning sign of contamination.")


if __name__ == "__main__":
    main()
