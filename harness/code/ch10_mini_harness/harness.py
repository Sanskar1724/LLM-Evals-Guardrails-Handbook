"""
Chapter 10 - A mini agent harness in one file.

Run:  python harness.py

The agent gets a small coding task: fix a bug in calc.py so the tests pass.
Everything a real harness does is here in small form:

  * the loop                (chapter 2)
  * tools with checks       (chapter 3)
  * short tool results      (chapter 4)
  * a sandboxed workspace   (chapter 7)
  * step limit, loop detection, "verify before done", and a trace (chapter 8)

The model is a mock (plain Python that picks the next step), so the run is
the same every time and needs no key. The mock makes two mistakes on purpose:
it tries to finish without testing, and its first fix is incomplete.
Watch how the HARNESS catches both.

It only writes inside a temporary folder.
"""

import json
import os
import tempfile

MAX_STEPS = 12
MAX_RESULT_CHARS = 400

BUGGY_FILE = '''def average(numbers):
    """Return the average of a list. An empty list gives 0."""
    return sum(numbers) / 2
'''

SYSTEM_PROMPT = (
    "You are a coding agent. Fix the task in the workspace. "
    "Reply with JSON: {\"thought\": ..., \"tool\": ..., \"args\": {...}}. "
    "Tools: list_files(), read_file(path), write_file(path, text), run_tests(), finish(summary). "
    "Call finish only after run_tests passes."
)


# ---------------- workspace and tools ----------------

class Workspace:
    def __init__(self):
        self.root = os.path.realpath(tempfile.mkdtemp())
        with open(os.path.join(self.root, "calc.py"), "w", encoding="utf-8") as file:
            file.write(BUGGY_FILE)
        self.tests_passed_since_last_write = False

    def _safe(self, path):
        full = os.path.realpath(os.path.join(self.root, path))
        if os.path.commonpath([full, self.root]) != self.root:
            raise PermissionError(f"'{path}' is outside the workspace")
        return full

    def list_files(self):
        return ", ".join(sorted(os.listdir(self.root)))

    def read_file(self, path):
        with open(self._safe(path), encoding="utf-8") as file:
            return file.read()

    def write_file(self, path, text):
        with open(self._safe(path), "w", encoding="utf-8") as file:
            file.write(text)
        self.tests_passed_since_last_write = False       # any edit makes old test results worthless
        return f"wrote {path}"

    def run_tests(self):
        """The harness runs the checks itself. It does not ask the model if the code works."""
        namespace = {}
        try:
            exec(self.read_file("calc.py"), namespace)   # fine here: our own tiny file in a temp folder
            average = namespace["average"]
            cases = [([2, 4, 6], 4), ([5], 5), ([], 0)]
            for numbers, expected in cases:
                got = average(numbers)
                if got != expected:
                    return f"FAIL: average({numbers}) returned {got}, expected {expected}"
        except Exception as error:                       # report any crash as a test failure
            return f"FAIL: average raised {type(error).__name__}: {error}"
        self.tests_passed_since_last_write = True
        return "PASS: 3 of 3 tests passed"


TOOL_ARGS = {
    "list_files": [],
    "read_file": ["path"],
    "write_file": ["path", "text"],
    "run_tests": [],
    "finish": ["summary"],
}


def call_tool(workspace, name, args):
    """Check the request, run it, and always return text. Errors become messages for the model."""
    if name not in TOOL_ARGS:
        return f"ERROR: unknown tool '{name}'. Tools: {', '.join(TOOL_ARGS)}."
    missing = [a for a in TOOL_ARGS[name] if a not in args]
    if missing:
        return f"ERROR: missing argument(s) {missing} for {name}."
    if name == "finish":
        if not workspace.tests_passed_since_last_write:
            return "REFUSED: you may only finish after run_tests passes on the current files. Call run_tests."
        return "FINISHED"
    try:
        result = str(getattr(workspace, name)(**{a: args[a] for a in TOOL_ARGS[name]}))
    except PermissionError as error:
        return "BLOCKED BY SANDBOX: " + str(error)
    except FileNotFoundError:
        return "ERROR: file not found. Call list_files to see what exists."
    if len(result) > MAX_RESULT_CHARS:
        result = result[:MAX_RESULT_CHARS] + f"... [cut: {len(result)} characters in total]"
    return result


# ---------------- the mock model ----------------

FIRST_FIX = '''def average(numbers):
    """Return the average of a list. An empty list gives 0."""
    return sum(numbers) / len(numbers)
'''

SECOND_FIX = '''def average(numbers):
    """Return the average of a list. An empty list gives 0."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
'''


def mock_model(messages):
    """Picks the next step from the conversation so far. A real LLM would do this by reading it."""
    calls = [json.loads(m["content"]) for m in messages if m["role"] == "assistant"]
    last_tool = calls[-1]["tool"] if calls else None
    last_result = messages[-1]["content"]
    writes = sum(1 for c in calls if c["tool"] == "write_file")

    if last_tool is None:
        return {"thought": "See what files exist.", "tool": "list_files", "args": {}}
    if last_tool == "list_files":
        return {"thought": "Read the file with the bug.", "tool": "read_file", "args": {"path": "calc.py"}}
    if last_tool == "read_file":
        return {"thought": "It divides by 2, not by the count. Fix that.",
                "tool": "write_file", "args": {"path": "calc.py", "text": FIRST_FIX}}
    if last_tool == "write_file" and writes == 1:
        return {"thought": "That should do it. I am done.",                      # mistake 1: no test
                "tool": "finish", "args": {"summary": "Fixed the division."}}
    if last_tool == "write_file":
        return {"thought": "Test the new version.", "tool": "run_tests", "args": {}}
    if last_tool == "finish":                                                    # the harness refused
        return {"thought": "I must run the tests first.", "tool": "run_tests", "args": {}}
    if last_tool == "run_tests" and last_result.startswith("PASS"):
        return {"thought": "Tests pass. Now I can finish.",
                "tool": "finish", "args": {"summary": "average() now divides by the count and handles empty lists."}}
    return {"thought": "The empty list crashes. Handle that case.",              # mistake 2 gets fixed
            "tool": "write_file", "args": {"path": "calc.py", "text": SECOND_FIX}}


# ---------------- the loop ----------------

def tokens(text):
    return max(1, len(text) // 4)


def run(task, model, workspace=None, max_steps=MAX_STEPS, verbose=True):
    """Returns a dict with status, summary, steps, trace and the workspace."""
    workspace = workspace or Workspace()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": task}]
    trace = []
    recent_actions = []

    for step in range(1, max_steps + 1):
        reply = model(messages)
        tokens_in = sum(tokens(m["content"]) for m in messages)

        if not isinstance(reply, dict) or "tool" not in reply:
            result = "ERROR: reply must be JSON with a 'tool' field."
            reply = {"thought": "", "tool": "(invalid)", "args": {}}
        else:
            action = json.dumps([reply["tool"], reply.get("args", {})], sort_keys=True)
            recent_actions.append(action)
            if recent_actions[-3:].count(action) == 3:
                result = "STOPPED BY HARNESS: the same action was repeated 3 times."
                trace.append({"step": step, "tool": reply["tool"], "result": result, "tokens_in": tokens_in})
                return {"status": "loop", "summary": result, "steps": step, "trace": trace, "workspace": workspace}
            result = call_tool(workspace, reply["tool"], reply.get("args", {}))

        messages.append({"role": "assistant", "content": json.dumps(reply)})
        messages.append({"role": "tool", "content": result})
        trace.append({"step": step, "tool": reply["tool"], "result": result, "tokens_in": tokens_in})
        if verbose:
            print(f"step {step}: {reply.get('thought', '')}")
            print(f"        {reply['tool']} -> {result.splitlines()[0][:90]}")

        if result == "FINISHED":
            return {"status": "finished", "summary": reply["args"]["summary"], "steps": step,
                    "trace": trace, "workspace": workspace}

    return {"status": "step_limit", "summary": "STOPPED BY HARNESS: step limit reached.",
            "steps": max_steps, "trace": trace, "workspace": workspace}


def main():
    task = "The function average() in calc.py is wrong. Fix it so that the tests pass."
    print("TASK:", task)
    print()
    outcome = run(task, mock_model)
    print()
    print("STATUS :", outcome["status"])
    print("SUMMARY:", outcome["summary"])
    print("STEPS  :", outcome["steps"])
    print("TOKENS SENT TO THE MODEL (all steps):", sum(e["tokens_in"] for e in outcome["trace"]))
    print()
    print("Final check by the harness, not by the agent:", outcome["workspace"].run_tests())
    print()
    print("Two things the harness did that the model did not want:")
    print("  step 4: refused 'finish' because no test had passed yet")
    print("  step 5: the test FAILED, and the failure went back to the model as feedback")


if __name__ == "__main__":
    main()
