"""
Chapter 5 - Memory: compaction and notes that survive a fresh start.

Run:  python ch05_memory.py

A model has no memory between calls. Everything it "remembers" is text
that the harness puts back into the context.

Part 1: compaction - when the conversation gets long, replace the old part
        with a short summary and keep the newest messages.
Part 2: notes on disk - the agent writes progress to a file. A new session
        (empty context) reads the file and continues where the last one stopped.

The summariser is a mock (it keeps lines that look important). With
OPENROUTER_API_KEY set, a real free model writes the summary (1 request).
"""

import json
import os
import tempfile

from llm_client import ask_llm


def tokens(text):
    return max(1, len(text) // 4)


def total_tokens(messages):
    return sum(tokens(m["content"]) for m in messages)


# ---------- Part 1: compaction ----------

def mock_summariser(prompt):
    """Keeps lines that contain decisions, file names or open problems."""
    log_lines = [line for line in prompt.splitlines() if line.startswith(("user:", "assistant:"))]
    keep = [line for line in log_lines
            if any(word in line.lower() for word in ("decided", "bug", "todo", "must", "build"))]
    return "Summary of earlier work:\n" + "\n".join("- " + line.split(": ", 1)[-1] for line in keep[:8])


def compact(messages, limit, keep_last=2):
    """If over the limit: summarise everything except the system prompt and the last few messages."""
    if total_tokens(messages) <= limit:
        return messages, False
    system, old, recent = messages[0], messages[1:-keep_last], messages[-keep_last:]
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
    summary = ask_llm(
        "Summarise this work log in at most 8 short bullet points. Keep decisions, file names, "
        "open bugs and next steps. Drop small talk.\n\n" + transcript,
        mock=mock_summariser, max_tokens=250)
    return [system, {"role": "user", "content": summary}] + recent, True


# ---------- Part 2: notes on disk ----------

def load_notes(path):
    if not os.path.exists(path):
        return {"done": [], "todo": ["write parser", "write tests", "write docs"], "facts": []}
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def save_notes(path, notes):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2)


def work_session(path, session_name, steps_possible):
    """One 'session' = one context window. It starts by reading the notes."""
    notes = load_notes(path)
    print(f"  {session_name}: starts with done={notes['done']} todo={notes['todo']}")
    for _ in range(steps_possible):
        if not notes["todo"]:
            break
        task = notes["todo"].pop(0)                 # work on ONE thing at a time
        notes["done"].append(task)
        notes["facts"].append(f"{task}: finished in {session_name}")
        save_notes(path, notes)                     # save after every step, not only at the end
    print(f"  {session_name}: ends   with done={notes['done']} todo={notes['todo']}")


def main():
    print("PART 1 - compaction")
    messages = [{"role": "system", "content": "You are a coding agent."}]
    log = [
        ("user", "Please build a CSV parser in parser.py"),
        ("assistant", "We decided to use the csv module, not regex."),
        ("tool", "ran tests: 3 passed " + "." * 600),
        ("assistant", "Found a bug: empty lines crash the parser. TODO fix in parser.py"),
        ("tool", "listing: " + "abc.py " * 150),
        ("user", "Also the output must be UTF-8."),
        ("assistant", "Nice weather today, by the way."),
        ("tool", "ran tests: 4 passed " + "." * 600),
        ("user", "What is left to do?"),
    ]
    messages += [{"role": role, "content": content} for role, content in log]
    before = total_tokens(messages)
    compacted, changed = compact(messages, limit=200)
    print(f"  before: {before} tokens, {len(messages)} messages")
    print(f"  after : {total_tokens(compacted)} tokens, {len(compacted)} messages (compacted={changed})")
    print("  " + compacted[1]["content"].replace("\n", "\n  "))
    print("  Note what was lost: the test output and the file listing. A summary always loses something.")

    print()
    print("PART 2 - notes that survive a new session")
    path = os.path.join(tempfile.mkdtemp(), "progress.json")
    work_session(path, "session 1", steps_possible=2)     # runs out of room after 2 steps
    work_session(path, "session 2", steps_possible=2)     # fresh context, same notes file
    print("  Session 2 knew nothing except what was in the file. That was enough.")


if __name__ == "__main__":
    main()
