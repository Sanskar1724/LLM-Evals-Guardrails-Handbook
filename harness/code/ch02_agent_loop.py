"""
Chapter 2 - The agent loop, in its smallest form.

Run:  python ch02_agent_loop.py

A harness is the code around the model. Its heart is one loop:

    1. send the conversation to the model
    2. the model answers with a tool call OR a final answer
    3. if it is a tool call: run the tool, add the result to the conversation, go to 1
    4. if it is a final answer: stop

The "model" here is a mock: plain Python that decides the next step.
So the script needs no key. The LOOP is real and is the thing to study.
"""

import json


# ---------- tools ----------

def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


TOOLS = {"add": add, "multiply": multiply}


# ---------- a mock model ----------

def mock_model(messages):
    """
    Pretends to be an LLM solving: (12 + 30) * 2
    It looks at how many tool results it has seen and picks the next step.
    A real model would read the whole conversation and decide by itself.
    """
    results = [m["content"] for m in messages if m["role"] == "tool"]
    if len(results) == 0:
        return {"thought": "First add 12 and 30.", "tool": "add", "args": {"a": 12, "b": 30}}
    if len(results) == 1:
        return {"thought": "Now multiply the sum by 2.", "tool": "multiply", "args": {"a": int(results[0]), "b": 2}}
    return {"thought": "I have the result.", "final": "The answer is " + results[1] + "."}


# ---------- the loop (this is the harness) ----------

def run_agent(task, model, max_steps=5):
    messages = [
        {"role": "system", "content": "You are a careful assistant. Use tools for all maths."},
        {"role": "user", "content": task},
    ]
    for step in range(1, max_steps + 1):
        reply = model(messages)                         # 1. ask the model
        print(f"step {step}: thought: {reply['thought']}")
        messages.append({"role": "assistant", "content": json.dumps(reply)})

        if "final" in reply:                            # 4. finished
            return reply["final"], messages

        tool = TOOLS[reply["tool"]]                     # 3. run the tool
        result = tool(**reply["args"])
        print(f"         tool:    {reply['tool']}({reply['args']}) -> {result}")
        messages.append({"role": "tool", "content": str(result)})

    return "STOPPED: step limit reached", messages      # safety net


def stuck_model(messages):
    """A model that never finishes. Shows why the step limit matters."""
    return {"thought": "Let me add again.", "tool": "add", "args": {"a": 1, "b": 1}}


def main():
    print("TASK: What is (12 + 30) * 2 ?")
    answer, messages = run_agent("What is (12 + 30) * 2 ?", mock_model)
    print("FINAL:", answer)
    print("messages in the conversation:", len(messages))

    print()
    print("A STUCK MODEL with max_steps=3")
    answer, _ = run_agent("Loop forever", stuck_model, max_steps=3)
    print("FINAL:", answer)


if __name__ == "__main__":
    main()
