"""
Chapter 4 - LLM-as-judge.

Run:  python ch04_llm_judge.py

An "LLM judge" is a model that reads an answer and gives it a grade.
This script:
  1. builds a judge prompt with a clear rubric (PASS / FAIL)
  2. sends each example to the judge
  3. compares the judge with human labels (agreement and Cohen's kappa)

With no key, a simple mock judge is used, so the script always runs.
With OPENROUTER_API_KEY set, a real free model is the judge.
This uses 8 requests. Free OpenRouter accounts have a small daily limit.
"""

import json
import re

from llm_client import ask_llm

JUDGE_PROMPT = """You are grading an answer from a customer support bot.

Question: {question}
Reference answer (correct): {reference}
Bot answer: {answer}

Rubric:
- PASS if the bot answer agrees with the reference answer on the key fact.
- FAIL if the key fact is missing, wrong, or contradicted.
- Do not reward long answers. Do not punish short answers.

First think in one short sentence. Then give the verdict.
Reply with JSON only, like this:
{{"reason": "one short sentence", "verdict": "PASS"}}
"""

# Small test set. "human" is the label a careful person gave.
EXAMPLES = [
    {"question": "How long do refunds take?",
     "reference": "Refunds take 5 working days.",
     "answer": "You will get your refund in 5 working days.",
     "human": "PASS"},
    {"question": "How long do refunds take?",
     "reference": "Refunds take 5 working days.",
     "answer": "Refunds are instant.",
     "human": "FAIL"},
    {"question": "What is the delivery fee?",
     "reference": "Delivery costs 40 rupees.",
     "answer": "The delivery fee is 40 rupees for all orders.",
     "human": "PASS"},
    {"question": "What is the delivery fee?",
     "reference": "Delivery costs 40 rupees.",
     "answer": "Thank you for asking! We love our customers and delivery is very fast.",
     "human": "FAIL"},
    {"question": "Can I change my address after ordering?",
     "reference": "Yes, within 2 hours of ordering.",
     "answer": "Yes. You can change it within 2 hours.",
     "human": "PASS"},
    {"question": "Can I change my address after ordering?",
     "reference": "Yes, within 2 hours of ordering.",
     "answer": "No, the address can never be changed.",
     "human": "FAIL"},
    # Two tricky cases. A weak judge gets these wrong.
    {"question": "How long do refunds take?",
     "reference": "Refunds take 5 working days.",
     "answer": "It needs five business days.",
     "human": "PASS"},
    {"question": "How long do refunds take?",
     "reference": "Refunds take 5 working days.",
     "answer": "Refunds never take 5 working days. Refunds take 10 working days.",
     "human": "FAIL"},
]


def mock_judge(prompt):
    """
    A fake judge for when there is no key.
    Rule: PASS if every number in the reference is also in the answer,
    and at least half of the reference's longer words appear in the answer.
    A real LLM judge understands meaning much better than this.
    """
    reference = re.search(r"Reference answer \(correct\): (.*)", prompt).group(1)
    answer = re.search(r"Bot answer: (.*)", prompt).group(1)

    ref_numbers = set(re.findall(r"\d+", reference))
    ans_numbers = set(re.findall(r"\d+", answer))
    ref_words = {w for w in re.findall(r"[a-z]+", reference.lower()) if len(w) > 3}
    ans_words = set(re.findall(r"[a-z]+", answer.lower()))
    word_share = len(ref_words & ans_words) / max(1, len(ref_words))

    ok = ref_numbers <= ans_numbers and word_share >= 0.5
    verdict = "PASS" if ok else "FAIL"
    return json.dumps({"reason": f"mock rule: numbers ok={ref_numbers <= ans_numbers}, word share={word_share:.2f}",
                       "verdict": verdict})


def parse_verdict(raw_text):
    """
    Get PASS or FAIL out of the judge's reply.
    Models do not always follow the format, so we parse with care.
    """
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            verdict = str(json.loads(match.group(0)).get("verdict", "")).upper()
            if verdict in ("PASS", "FAIL"):
                return verdict
        except json.JSONDecodeError:
            pass
    # Fallback: look for the word itself.
    upper = raw_text.upper()
    if "PASS" in upper and "FAIL" not in upper:
        return "PASS"
    if "FAIL" in upper and "PASS" not in upper:
        return "FAIL"
    return "UNKNOWN"


def cohens_kappa(labels_a, labels_b):
    """
    Agreement between two graders, corrected for luck.
    1.0 = perfect agreement, 0 = no better than chance.
    """
    n = len(labels_a)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / n
    categories = set(labels_a) | set(labels_b)
    expected = sum(
        (labels_a.count(c) / n) * (labels_b.count(c) / n) for c in categories
    )
    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1 - expected)


def main():
    judge_labels = []
    human_labels = []
    for number, example in enumerate(EXAMPLES, start=1):
        prompt = JUDGE_PROMPT.format(**example)
        raw = ask_llm(prompt, mock=mock_judge, max_tokens=120)
        verdict = parse_verdict(raw)
        judge_labels.append(verdict)
        human_labels.append(example["human"])
        mark = "same" if verdict == example["human"] else "DIFFERENT"
        print(f"{number}. judge={verdict:7} human={example['human']:4} ({mark})  answer: {example['answer'][:50]}")

    agreement = sum(j == h for j, h in zip(judge_labels, human_labels)) / len(EXAMPLES)
    kappa = cohens_kappa(judge_labels, human_labels)
    print()
    print(f"Judge agrees with humans on {agreement:.0%} of examples.")
    print(f"Cohen's kappa = {kappa:.2f}")
    print("Check this agreement BEFORE you trust a judge on new data.")


if __name__ == "__main__":
    main()
