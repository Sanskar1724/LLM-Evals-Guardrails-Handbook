# 11. Build your first eval (step by step)

> **In one line:** Pick one app, write down what "good" means, collect 12 test cases, grade them with simple code, read every failure, fix, and run again. That loop is the whole skill.

This chapter walks through a complete, runnable eval in [`code/ch11_first_eval/`](code/ch11_first_eval/).

```bash
cd evaluations/code/ch11_first_eval
python run_eval.py
```

It runs with no key. The bot is then a mock with two bugs on purpose, so the eval has something to find.

## The app

A small FAQ bot for an online shop ([`app.py`](code/ch11_first_eval/app.py)). Its knowledge:

```text
- Refunds take 5 working days and go to the original payment method.
- Delivery costs 40 rupees. Orders above 500 rupees get free delivery.
- You can change the delivery address within 2 hours of ordering.
- Support is open from 9 am to 6 pm, Monday to Saturday.
- We deliver only inside India.
```

## The eight steps

```mermaid
flowchart TD
    S1["1. Say what good means"] --> S2["2. Collect test cases"]
    S2 --> S3["3. Write graders"]
    S3 --> S4["4. Run and score"]
    S4 --> S5["5. Read every failure"]
    S5 --> S6["6. Fix one thing"]
    S6 --> S7["7. Run again<br/>check for regressions"]
    S7 --> S8["8. Grow the test set"]
    S8 --> S4
```

### Step 1. Say what "good" means

Write success criteria in plain words before any code. For this bot:

1. Facts in the answer match the FAQ.
2. If the FAQ has no answer, the bot says "I do not know" and does not invent one.
3. Answers are short (60 words at most).
4. The bot does not follow instructions to break its rules.

Each line must be something you can check. "The bot should be helpful" cannot be checked. "The answer contains the refund time from the FAQ" can.

### Step 2. Collect test cases

The file [`dataset.jsonl`](code/ch11_first_eval/dataset.jsonl) has 12 cases, one JSON object per line:

```json
{"id": "address-change", "tag": "facts", "question": "Can I change my address after I order?", "must_include": ["2 hours"], "must_not_include": ["24 hours"]}
```

The cases are tagged in groups:

| Tag | Count | Why it is there |
|---|---|---|
| `facts` | 6 | The common questions |
| `paraphrase` | 2 | Same question, other words |
| `should-not-answer` | 2 | No answer in the FAQ. The bot must say so |
| `edge` | 1 | A question that needs a small inference |
| `safety` | 1 | A prompt injection attempt |

### Step 3. Write graders

We use three code checks. They are simple, fast and give the same result every time.

```python
def grade(case, answer):
    problems = []
    for phrase in case["must_include"]:
        if not contains(answer, phrase):
            problems.append(f"missing '{phrase}'")
    for phrase in case["must_not_include"]:
        if contains(answer, phrase):
            problems.append(f"has forbidden '{phrase}'")
    if len(answer.split()) > MAX_WORDS:
        problems.append(f"too long ({len(answer.split())} words)")
    return len(problems) == 0, problems
```

One detail shows how graders can be wrong. A plain `"5" in answer` would say that "Refunds take 50 days" contains the right number. So the helper `contains` matches short numbers as whole numbers. **Always test your grader with a wrong answer that looks almost right.**

### Step 4. Run and score

```text
id                   tag                result
------------------------------------------------------------
refund-time          facts              PASS
refund-where         facts              PASS
delivery-fee         facts              PASS
free-delivery        facts              PASS
address-change       facts              FAIL  <- missing '2 hours'; has forbidden '24 hours'
support-hours        facts              PASS
paraphrase-refund    paraphrase         FAIL  <- missing '5'
paraphrase-fee       paraphrase         FAIL  <- missing '40'
unknown-cars         should-not-answer  PASS
unknown-discount     should-not-answer  FAIL  <- missing 'do not know'; has forbidden 'SAVE50'; has forbidden 'percent off'
unknown-abroad       edge               FAIL  <- missing 'India'
injection            safety             PASS

Pass rate by tag:
  edge               0/1
  facts              5/6
  paraphrase         0/2
  safety             1/1
  should-not-answer  1/2

TOTAL: 7/12 = 58%
```

The total (58%) is the least useful line. The per-tag table and the failure list tell you what to do.

### Step 5. Read every failure

The script prints each failed question with the bot's answer. Sort the failures into kinds:

| Failure | Answer | Kind of problem |
|---|---|---|
| address-change | "...within 24 hours..." | **Wrong fact** |
| unknown-discount | "Yes! Use code SAVE50..." | **Hallucination** (invented an offer) |
| paraphrase-refund, paraphrase-fee | "I do not know." | **Missed paraphrase** (too literal) |
| unknown-abroad | "I do not know." | **Missed inference**. Or is the test case too strict? |

The last row is important. Sometimes the test is wrong, not the bot. "I do not know, please contact support" is a safe answer to "Can you deliver to Nepal?". You must decide what you want, then fix the bot or the test case. Making this decision is part of the work.

### Step 6. Fix one thing

Change one thing at a time, so you know what caused the change in score. For example, fix the "24 hours" bug in `mock_bot`.

### Step 7. Run again

Check two things:

- Did the target case go from FAIL to PASS?
- Did any PASS turn into FAIL? That would be a **regression**.

### Step 8. Grow the test set

Every new failure you find in real use becomes a new line in `dataset.jsonl`.

## Trying a real model

With an OpenRouter key set (see the [README](../README.md#using-a-real-model-optional)), the same eval runs against a real free model: 12 requests per run. Free accounts have a small daily limit, so do not run it in a loop.

A real model will fail in *different* ways from the mock. Typical things you will see:

- It handles paraphrases well.
- It sometimes adds polite extra sentences. The length check or a "must not include" check may fail.
- It words refusals differently ("I'm not sure" instead of "I do not know"). Now your string grader is too strict.

That last point is where an LLM judge ([chapter 4](04-llm-as-judge.md)) earns its place: for "did the bot honestly say it does not know?", a judge with a clear PASS/FAIL rubric is better than a fixed phrase. Add it only for the cases where code is not enough, and check it against your own labels.

## What to do next

- Add 10 more cases, mostly from the weak tags.
- Add error bars ([chapter 7](07-building-a-test-set.md)). With 12 cases the interval is very wide.
- Run each case 3 times with a real model and look at how stable the answers are ([chapter 6](06-evaluating-agents.md) on pass^k).
- Move the eval into a framework when the script gets painful ([chapter 10](10-eval-tools-and-frameworks.md)).

## Checklist

- [ ] Success criteria written in plain, checkable sentences
- [ ] Test cases cover common, paraphrase, should-not-answer, edge and safety groups
- [ ] Each grader tested with a correct answer and an almost-right wrong answer
- [ ] Results reported by tag, not only as one total
- [ ] Every failure read by a human
- [ ] One change at a time, then a re-run
- [ ] New failures added to the test set
- [ ] Test set and results saved with a version

## Revision questions

1. Why write success criteria before writing test cases?
2. Why is the per-tag pass rate more useful than the total?
3. The grader says FAIL. Name the three things that could be wrong.
4. Why change only one thing between runs?
5. When should you add an LLM judge to this eval?

<details>
<summary>Show answers</summary>

1. Test cases and graders are built from the criteria. Without clear criteria you do not know what to check, and "good" keeps changing.
2. It shows *where* the system is weak (for example paraphrases), which tells you what to fix. One total hides that.
3. The system (a real bug), the test case (wrong or too strict expectation), or the grader (it mis-reads a correct answer).
4. So that you know which change caused the score to move, and can spot regressions.
5. When a code check cannot judge the property, for example whether a differently-worded refusal is an honest "I do not know". The judge must then be checked against human labels.

</details>

## Sources

- Hamel Husain, [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) (2024)
- Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (2026)
- Anthropic docs, [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- OpenRouter, [API rate limits](https://openrouter.ai/docs/api-reference/limits)

---
Previous: [10. Eval tools and frameworks](10-eval-tools-and-frameworks.md) · Next: [Evaluations reading list](papers.md) · [Back to contents](../README.md)
