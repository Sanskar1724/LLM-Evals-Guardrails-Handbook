"""
Chapter 8 - Reliability: retries, loop detection, verification and traces.

Run:  python ch08_reliability.py

Things go wrong in every long agent run. A good harness expects that.

Part 1: retry a failing call a few times, waiting longer each time ("backoff").
Part 2: notice when the agent repeats the same action (a loop) and stop it.
Part 3: do not trust "I am done" - verify the result with a real check.
Part 4: write a trace (a log of every step) so you can debug later.

Time is simulated, so nothing really waits.

No key needed. Standard library only.
"""

import json


# ---------- Part 1: retries with backoff ----------

class FlakyService:
    """Fails the first `failures` times, then works. Like a busy API."""

    def __init__(self, failures):
        self.failures = failures
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise ConnectionError("429 too many requests")
        return "result"


def call_with_retries(function, max_tries=4, first_wait=1.0):
    """Returns (result, list of waits). Raises after the last failed try."""
    waits = []
    wait = first_wait
    for attempt in range(1, max_tries + 1):
        try:
            return function(), waits
        except ConnectionError:
            if attempt == max_tries:
                raise
            waits.append(wait)          # a real harness would sleep here
            wait *= 2                   # exponential backoff: 1s, 2s, 4s ...
    return None, waits


# ---------- Part 2: loop detection ----------

def is_looping(history, window=3):
    """True if the last `window` actions are identical."""
    if len(history) < window:
        return False
    last = history[-window:]
    return all(action == last[0] for action in last)


# ---------- Part 3: verification ----------

def buggy_sort(numbers):
    return numbers                      # the agent "forgot" to sort


def fixed_sort(numbers):
    return sorted(numbers)


def verify(function):
    """A real check, run by the harness. The agent's own claim does not count."""
    cases = [([3, 1, 2], [1, 2, 3]), ([], []), ([5, 5, 1], [1, 5, 5])]
    failed = [case for case, expected in cases if function(list(case)) != expected]
    return len(failed) == 0, failed


# ---------- Part 4: trace ----------

class Trace:
    def __init__(self):
        self.events = []

    def add(self, kind, **details):
        self.events.append({"step": len(self.events) + 1, "kind": kind, **details})

    def summary(self):
        kinds = {}
        for event in self.events:
            kinds[event["kind"]] = kinds.get(event["kind"], 0) + 1
        return kinds


def main():
    print("PART 1 - retries with backoff")
    result, waits = call_with_retries(FlakyService(failures=2))
    print(f"  fails twice, then works: result={result!r}, waited {waits} seconds")
    try:
        call_with_retries(FlakyService(failures=10))
    except ConnectionError as error:
        print(f"  always fails: gave up after 4 tries ({error}). Never retry forever.")

    print()
    print("PART 2 - loop detection")
    history = []
    for step, action in enumerate(["read a.py", "search 'bug'", "search 'bug'", "search 'bug'", "search 'bug'"], 1):
        history.append(action)
        if is_looping(history):
            print(f"  step {step}: '{action}' repeated 3 times -> stop and tell the model to try something else")
            break
        print(f"  step {step}: {action}")

    print()
    print("PART 3 - verify before accepting 'done'")
    for name, function in [("first attempt", buggy_sort), ("second attempt", fixed_sort)]:
        ok, failed = verify(function)
        claim = "agent says: done!"
        print(f"  {name}: {claim}  harness check: {'PASS' if ok else 'FAIL on ' + str(failed)}")
    print("  The failed check goes back to the model as feedback, and it tries again.")

    print()
    print("PART 4 - a trace of one run")
    trace = Trace()
    trace.add("model_call", tokens_in=820, tokens_out=40)
    trace.add("tool_call", tool="read_file", args={"path": "sort.py"}, ok=True, ms=3)
    trace.add("model_call", tokens_in=1150, tokens_out=95)
    trace.add("tool_call", tool="write_file", args={"path": "sort.py"}, ok=True, ms=4)
    trace.add("verify", passed=True)
    for event in trace.events:
        print("  " + json.dumps(event))
    total_in = sum(e.get("tokens_in", 0) for e in trace.events)
    print(f"  summary: {trace.summary()}  input tokens: {total_in}")
    print("  With a trace you can answer: what did it do, where did it fail, what did it cost?")


if __name__ == "__main__":
    main()
