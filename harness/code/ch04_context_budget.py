"""
Chapter 4 - Context engineering: fitting the right things into a limited window.

Run:  python ch04_context_budget.py

The model only knows what is in its context window (the text sent in one call).
The window is limited, and quality drops when it is full of noise.
So the harness chooses what goes in.

Part 1: count tokens and see what fills the window.
Part 2: build a context under a budget (keep what matters, drop old tool output).
Part 3: load a file "just in time" in small pieces, not all at once.

No key needed. Standard library only.
"""


def tokens(text):
    """Rough estimate: about 4 characters per token."""
    return max(1, len(text) // 4)


def total_tokens(messages):
    return sum(tokens(m["content"]) for m in messages)


def make_history():
    """A fake history: a few user turns and some very large tool results."""
    messages = [{"role": "system", "content": "You are a coding assistant. " * 10}]
    for turn in range(1, 7):
        messages.append({"role": "user", "content": f"Question {turn}: please check file_{turn}.py"})
        messages.append({"role": "tool", "content": f"[contents of file_{turn}.py] " + "x = 1\n" * 400})
        messages.append({"role": "assistant", "content": f"file_{turn}.py looks fine. Summary: defines x."})
    messages.append({"role": "user", "content": "Now compare file_5.py and file_6.py."})
    return messages


def build_context(messages, budget, keep_recent_tools=2):
    """
    Simple policy:
      * always keep the system prompt and all user and assistant messages
      * keep only the newest `keep_recent_tools` tool results in full
      * replace older tool results with a one-line note ("tool-result clearing")
    """
    tool_positions = [i for i, m in enumerate(messages) if m["role"] == "tool"]
    keep = set(tool_positions[-keep_recent_tools:])
    context = []
    for i, m in enumerate(messages):
        if m["role"] == "tool" and i not in keep:
            first_line = m["content"].split("]")[0] + "]"
            context.append({"role": "tool", "content": first_line + " (old result removed to save space; read the file again if needed)"})
        else:
            context.append(m)
    if total_tokens(context) > budget:
        raise ValueError("still over budget: summarise the conversation (see chapter 5)")
    return context


def read_file_slice(lines, start, count):
    """Just-in-time loading: return only a slice, and say how much more there is."""
    part = lines[start:start + count]
    more = len(lines) - (start + len(part))
    return "\n".join(part) + (f"\n[{more} more lines. Call again with start={start + count}]" if more > 0 else "")


def main():
    messages = make_history()
    print("PART 1 - what fills the window")
    by_role = {}
    for m in messages:
        by_role[m["role"]] = by_role.get(m["role"], 0) + tokens(m["content"])
    total = total_tokens(messages)
    for role, count in sorted(by_role.items(), key=lambda item: -item[1]):
        print(f"  {role:10} {count:6} tokens  ({count / total:.0%})")
    print(f"  {'TOTAL':10} {total:6} tokens")
    print("  Tool results are almost everything. This is normal for agents.")

    print()
    budget = 2000
    print(f"PART 2 - build a context under a budget of {budget} tokens")
    context = build_context(messages, budget)
    print(f"  before: {total} tokens in {len(messages)} messages")
    print(f"  after : {total_tokens(context)} tokens in {len(context)} messages")
    print("  example of a cleared result:", context[2]["content"])

    print()
    print("PART 3 - just-in-time loading")
    big_file = [f"line {n}: value = {n * n}" for n in range(1, 501)]
    whole = "\n".join(big_file)
    piece = read_file_slice(big_file, 0, 5)
    print(f"  whole file: {tokens(whole)} tokens.  first slice: {tokens(piece)} tokens")
    print("  " + piece.replace("\n", "\n  "))


if __name__ == "__main__":
    main()
