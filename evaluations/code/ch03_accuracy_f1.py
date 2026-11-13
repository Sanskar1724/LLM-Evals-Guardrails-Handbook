"""
Chapter 3 - Accuracy, precision, recall and F1.

Run:  python ch03_accuracy_f1.py

Part 1: a yes/no task (is this message spam?).
Part 2: a short-answer task (exact match and token F1).

No key needed. Standard library only.
"""


def confusion_counts(gold, predicted, positive="spam"):
    """Count the four cases for one 'positive' class."""
    tp = fp = fn = tn = 0
    for g, p in zip(gold, predicted):
        if p == positive and g == positive:
            tp += 1          # true positive: said spam, was spam
        elif p == positive and g != positive:
            fp += 1          # false positive: said spam, was NOT spam
        elif p != positive and g == positive:
            fn += 1          # false negative: missed a spam
        else:
            tn += 1          # true negative: said ok, was ok
    return tp, fp, fn, tn


def safe_divide(a, b):
    return a / b if b else 0.0


def scores(tp, fp, fn, tn):
    accuracy = safe_divide(tp + tn, tp + fp + fn + tn)
    precision = safe_divide(tp, tp + fp)   # of all "spam" calls, how many were right
    recall = safe_divide(tp, tp + fn)      # of all real spam, how many we found
    f1 = safe_divide(2 * precision * recall, precision + recall)
    return accuracy, precision, recall, f1


def exact_match(prediction, gold):
    """1 if the two answers are the same after simple cleaning, else 0."""
    return int(normalise(prediction) == normalise(gold))


def normalise(text):
    """Lower-case, remove punctuation and extra spaces."""
    kept = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
    return " ".join(kept.split())


def token_f1(prediction, gold):
    """F1 over shared words. Gives part marks for a partly right answer."""
    pred_tokens = normalise(prediction).split()
    gold_tokens = normalise(gold).split()
    remaining = list(gold_tokens)
    shared = 0
    for token in pred_tokens:
        if token in remaining:
            remaining.remove(token)
            shared += 1
    if shared == 0:
        return 0.0
    precision = shared / len(pred_tokens)
    recall = shared / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def main():
    print("PART 1 - spam filter")
    gold      = ["spam", "ok", "ok", "spam", "ok", "ok", "ok", "spam", "ok", "ok"]
    predicted = ["spam", "ok", "spam", "ok", "ok", "ok", "ok", "spam", "ok", "ok"]
    tp, fp, fn, tn = confusion_counts(gold, predicted)
    print(f"  TP={tp} FP={fp} FN={fn} TN={tn}")
    accuracy, precision, recall, f1 = scores(tp, fp, fn, tn)
    print(f"  accuracy={accuracy:.2f} precision={precision:.2f} recall={recall:.2f} F1={f1:.2f}")

    print()
    print("PART 1b - why accuracy alone can fool you")
    # 95 normal messages, 5 spam. A lazy model says "ok" every time.
    gold = ["ok"] * 95 + ["spam"] * 5
    lazy = ["ok"] * 100
    tp, fp, fn, tn = confusion_counts(gold, lazy)
    accuracy, precision, recall, f1 = scores(tp, fp, fn, tn)
    print(f"  lazy model: accuracy={accuracy:.2f} but recall={recall:.2f} and F1={f1:.2f}")
    print("  It never finds any spam, yet accuracy looks great.")

    print()
    print("PART 2 - short answers")
    pairs = [
        ("Paris", "Paris"),
        ("The capital is Paris.", "Paris"),
        ("London", "Paris"),
    ]
    for prediction, gold_answer in pairs:
        em = exact_match(prediction, gold_answer)
        f1 = token_f1(prediction, gold_answer)
        print(f"  prediction={prediction!r:28} gold={gold_answer!r:8} exact_match={em} token_F1={f1:.2f}")


if __name__ == "__main__":
    main()
