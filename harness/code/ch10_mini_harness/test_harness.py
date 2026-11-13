"""
Chapter 10 - Tests for the mini harness.

Run:  python test_harness.py

A harness is normal software, so it gets normal tests.
Each test uses a different mock model to push the harness into one situation.
We check the OUTCOME (the real file and the real test result), not what the agent says.
"""

from harness import Workspace, call_tool, mock_model, run


def check(name, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    return condition


def stuck_model(messages):
    return {"thought": "again", "tool": "list_files", "args": {}}


def wandering_model(messages):
    """Never repeats itself and never finishes."""
    step = sum(1 for m in messages if m["role"] == "assistant")
    return {"thought": "reading", "tool": "read_file", "args": {"path": f"file_{step}.py"}}


def lazy_model(messages):
    """Claims to be done at once."""
    return {"thought": "done", "tool": "finish", "args": {"summary": "All fixed, trust me."}}


def main():
    results = []

    outcome = run("fix calc.py", mock_model, verbose=False)
    results.append(check("normal run finishes", outcome["status"] == "finished"))
    results.append(check("outcome: tests really pass at the end",
                         outcome["workspace"].run_tests().startswith("PASS")))
    results.append(check("finish was refused before any test passed",
                         any(e["tool"] == "finish" and e["result"].startswith("REFUSED") for e in outcome["trace"])))
    results.append(check("a failing test was reported back to the model",
                         any(e["tool"] == "run_tests" and e["result"].startswith("FAIL") for e in outcome["trace"])))
    results.append(check("every step is in the trace", len(outcome["trace"]) == outcome["steps"]))

    outcome = run("fix calc.py", stuck_model, verbose=False)
    results.append(check("loop detection stops a repeating model", outcome["status"] == "loop" and outcome["steps"] == 3))

    outcome = run("fix calc.py", wandering_model, max_steps=5, verbose=False)
    results.append(check("step limit stops a model that never finishes", outcome["status"] == "step_limit"))

    outcome = run("fix calc.py", lazy_model, max_steps=4, verbose=False)
    results.append(check("a model that only claims success never finishes",
                         outcome["status"] != "finished" and not outcome["workspace"].tests_passed_since_last_write))

    workspace = Workspace()
    results.append(check("sandbox blocks reading outside the workspace",
                         call_tool(workspace, "read_file", {"path": "../../secret.txt"}).startswith("BLOCKED")))
    results.append(check("sandbox blocks writing outside the workspace",
                         call_tool(workspace, "write_file", {"path": "../evil.py", "text": "x"}).startswith("BLOCKED")))
    results.append(check("unknown tool gives an error message, not a crash",
                         call_tool(workspace, "delete_all", {}).startswith("ERROR")))
    results.append(check("missing argument gives an error message, not a crash",
                         call_tool(workspace, "read_file", {}).startswith("ERROR")))

    workspace = Workspace()
    call_tool(workspace, "write_file", {"path": "calc.py", "text": "def average(n):\n    return 0 if not n else sum(n) / len(n)\n"})
    call_tool(workspace, "run_tests", {})
    call_tool(workspace, "write_file", {"path": "calc.py", "text": "def average(n):\n    return 1\n"})
    results.append(check("an edit after a passing test makes 'finish' refused again",
                         call_tool(workspace, "finish", {"summary": "x"}).startswith("REFUSED")))

    print()
    print(f"{sum(results)}/{len(results)} tests passed")
    raise SystemExit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
