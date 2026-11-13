"""
Chapter 6 - Planning and sub-agents.

Run:  python ch06_subagents.py

A sub-agent is a second agent loop with its OWN, clean context.
The main agent (the "orchestrator") gives it one clear job.
The sub-agent does a lot of reading and returns only a short summary.

Why: the long, noisy work stays out of the main agent's context.
Cost: more model calls and more total tokens.

Here all "models" are mocks, so no key is needed. We count tokens to show
the trade-off: the main context stays small, the total work gets bigger.
"""

DOCUMENTS = {
    "refunds.txt": "Refund policy. " + "Refunds take 5 working days. " * 60,
    "delivery.txt": "Delivery policy. " + "Delivery costs 40 rupees. " * 60,
    "support.txt": "Support hours. " + "Support is open 9 am to 6 pm. " * 60,
}


def tokens(text):
    return max(1, len(text) // 4)


def run_subagent(job, file_name):
    """
    A sub-agent: fresh context, one job, short answer back.
    Returns (summary, tokens_used_inside).
    """
    context = [f"Your only job: {job}", "Reply in one short sentence."]
    document = DOCUMENTS[file_name]                 # the sub-agent reads the whole file
    context.append(document)
    key_sentence = document.split(". ")[1] + "."    # mock "reading": pick the fact
    summary = f"{file_name}: {key_sentence}"
    used = sum(tokens(part) for part in context) + tokens(summary)
    return summary, used


def plan(question):
    """The orchestrator's plan: which files matter, and one job for each."""
    jobs = []
    if "refund" in question:
        jobs.append(("Find how long refunds take.", "refunds.txt"))
    if "delivery" in question:
        jobs.append(("Find the delivery fee.", "delivery.txt"))
    if "support" in question:
        jobs.append(("Find the support hours.", "support.txt"))
    return jobs


def answer_alone(question):
    """One agent reads every needed file into its own context."""
    context = [question] + [DOCUMENTS[file_name] for _job, file_name in plan(question)]
    return sum(tokens(part) for part in context)


def answer_with_subagents(question):
    """The orchestrator only sees the question, the plan and the short summaries."""
    main_context = [question]
    total_used = 0
    for job, file_name in plan(question):
        summary, used = run_subagent(job, file_name)
        main_context.append(summary)                # only the summary comes back
        total_used += used
    main_tokens = sum(tokens(part) for part in main_context)
    return main_context, main_tokens, total_used + main_tokens


def main():
    question = "What is the refund time, the delivery fee and the support hours?"
    print("QUESTION:", question)
    print()

    alone = answer_alone(question)
    print("ONE AGENT ALONE")
    print(f"  tokens in its context: {alone}")

    print()
    main_context, main_tokens, total = answer_with_subagents(question)
    print("ORCHESTRATOR + 3 SUB-AGENTS")
    for line in main_context[1:]:
        print("  got back:", line)
    print(f"  tokens in the MAIN context: {main_tokens}")
    print(f"  tokens used in TOTAL      : {total}")

    print()
    print(f"The main context is {alone / main_tokens:.0f} times smaller, so the orchestrator stays focused.")
    print(f"But the total is {total / alone:.2f} times the single-agent cost, and each sub-agent is an extra model call.")
    print("Sub-agents can also run at the same time, which saves waiting time.")
    print()
    print("Risk: a sub-agent only knows what its job text says. A vague job gives a useless answer.")


if __name__ == "__main__":
    main()
