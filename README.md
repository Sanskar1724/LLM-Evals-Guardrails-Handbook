# LLM Evals and Guardrails Handbook

A simple, student-friendly handbook on **evaluating LLMs** and **adding guardrails to LLM apps**, with diagrams, runnable code and revision questions.

- Written in plain, simple English.
- Every chapter has a one-line summary, key terms, a diagram, and revision questions with answers.
- Every code example runs on a weak laptop: CPU only, no paid service, **no API key needed**.

## Who it is for

Undergraduate students and beginners who know a little Python and want to understand how LLM apps are tested and made safer.

## How to use it for revision

1. Read the "In one line" box at the top of a chapter.
2. Read the chapter and run its code.
3. Cover the answers and try the revision questions at the end.
4. Come back a few days later and do only the questions.

## Contents

### Part 1: Evaluations

1. [Why evaluate?](evaluations/01-why-evaluate.md)
2. [Kinds of evals](evaluations/02-kinds-of-evals.md)
3. [Classic metrics](evaluations/03-classic-metrics.md) (accuracy, F1, BLEU, ROUGE, BERTScore, perplexity)
4. [LLM-as-judge](evaluations/04-llm-as-judge.md)
5. [Evaluating RAG](evaluations/05-evaluating-rag.md)
6. [Evaluating agents and tool use](evaluations/06-evaluating-agents.md)
7. [Building a test set](evaluations/07-building-a-test-set.md)
8. [Safety and red-team evals](evaluations/08-safety-and-red-team-evals.md)
9. [Common benchmarks and their limits](evaluations/09-benchmarks-and-their-limits.md)
10. [Eval tools and frameworks](evaluations/10-eval-tools-and-frameworks.md)
11. [Build your first eval](evaluations/11-build-your-first-eval.md)
- [Reading list](evaluations/papers.md)

### Part 2: Guardrails

1. [What guardrails are and where they sit](guardrails/01-what-are-guardrails.md)
2. [Prompt injection and jailbreaks](guardrails/02-prompt-injection-and-jailbreaks.md)
3. [PII and sensitive data](guardrails/03-pii-and-sensitive-data.md)
4. [Toxicity and content moderation](guardrails/04-toxicity-and-content-moderation.md)
5. [Hallucination checks and grounding](guardrails/05-hallucination-and-grounding.md)
6. [Structured-output validation](guardrails/06-structured-output-validation.md)
7. [Rate limits and cost limits](guardrails/07-rate-limits-and-cost-limits.md)
8. [Human-in-the-loop](guardrails/08-human-in-the-loop.md)
9. [Guardrail tools and frameworks](guardrails/09-guardrail-tools-and-frameworks.md)
10. [The OWASP Top 10 for LLM applications](guardrails/10-owasp-top-10-for-llm-apps.md)
11. [How guardrails are evaluated](guardrails/11-evaluating-guardrails.md)
12. [Add guardrails to a small app](guardrails/12-add-guardrails-to-a-small-app.md)
- [Reading list](guardrails/papers.md)

### Suggested order

Read Part 1 chapters 1 to 4 first. After that the two parts can be read in any order. Guardrails chapter 11 uses ideas from Part 1 chapter 3.

## How to run the code

You need Python 3.10 or newer. Nothing to install (one optional example needs `pip install pydantic`).

```bash
cd evaluations/code
python ch03_bleu_rouge.py
```

```bash
cd guardrails/code
python ch02_injection_filter.py
```

File names start with the chapter number, for example `ch05_rag_metrics.py` belongs to chapter 5.

## Using a real model (optional)

All examples use a mock (fake) model by default. To try a real free model, make a free key at [openrouter.ai](https://openrouter.ai) and set it in your terminal. Never put the key in a file that you commit.

Windows PowerShell:

```powershell
$env:OPENROUTER_API_KEY = "your-key-here"
```

Linux or macOS:

```bash
export OPENROUTER_API_KEY="your-key-here"
```

Free OpenRouter accounts are limited to about 50 requests per day, so run real-model examples only once or twice. If a call fails, the code falls back to the mock.

## Which examples were run

All of these were run on Windows 11 with Python 3.14, with no key (mock model), and finished without errors:

- `evaluations/code`: `llm_client.py`, `ch03_accuracy_f1.py`, `ch03_bleu_rouge.py`, `ch03_perplexity.py`, `ch03_bertscore_idea.py`, `ch04_llm_judge.py`, `ch05_rag_metrics.py`, `ch06_agent_eval.py`, `ch07_error_bars.py`, `ch08_red_team_eval.py`, `ch09_contamination_check.py`, `ch11_first_eval/run_eval.py`
- `guardrails/code`: `ch01_guard_pipeline.py`, `ch02_injection_filter.py`, `ch03_pii_redaction.py`, `ch04_moderation_filter.py`, `ch05_grounding_check.py`, `ch06_structured_output.py`, `ch06_structured_output_pydantic.py`, `ch07_rate_and_cost_limits.py`, `ch08_human_approval.py`, `ch11_evaluate_guardrail.py`, `ch12_guarded_app/app.py`, `ch12_guarded_app/test_app.py` (11 of 11 tests pass)

**Not tested:** a real OpenRouter call with a valid key. Only the fallback was tested (a wrong key correctly falls back to the mock).

## About the sources

Every paper and document linked in this handbook was checked to exist when it was written (November 2026). Tools and services in this area change quickly, so check the linked pages for current details. Summaries are in our own words. Diagrams were drawn for this handbook.

## Found a mistake?

Open an issue or a pull request. Corrections are welcome.

## Licence

- Code: [MIT](LICENSE)
- Text and diagrams: [CC BY 4.0](LICENSE-TEXT.md)
