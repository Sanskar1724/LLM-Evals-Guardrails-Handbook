"""
Chapter 6 - Evaluating an agent that uses tools.

Run:  python ch06_agent_eval.py

An agent is a model that works in a loop: it picks a tool, reads the result,
and repeats until the job is done.

Here the "agent" is a small rule-based mock, so no key is needed.
It is a little unreliable on purpose (it sometimes skips a step),
so that you can see why we run each task more than once.

We grade three things:
  1. outcome   - is the final state of the "database" correct?
  2. tool use  - were the needed tools called, and no forbidden tool?
  3. cost      - how many steps did it take?

Then we show pass@k and pass^k.
"""

import copy
import random

START_DATABASE = {
    "orders": {
        "A1": {"item": "book", "price": 300, "status": "delivered"},
        "A2": {"item": "lamp", "price": 900, "status": "shipped"},
    },
    "refunds": [],
}


# ---------- the tools the agent may call ----------

def tool_get_order(db, order_id):
    return db["orders"].get(order_id)


def tool_refund(db, order_id):
    order = db["orders"][order_id]
    db["refunds"].append({"order": order_id, "amount": order["price"]})
    order["status"] = "refunded"
    return "refund done"


def tool_delete_order(db, order_id):
    del db["orders"][order_id]
    return "deleted"


# ---------- the mock agent ----------

def mock_agent(task_text, db, rng):
    """
    Returns the list of tool calls it made (the "trajectory").
    Policy rule it should follow: only refund orders that are delivered.
    With some probability it forgets to check the order first.
    """
    trajectory = []
    order_id = "A1" if "A1" in task_text else "A2"

    careless = rng.random() < 0.25          # 25% of runs are careless
    if not careless:
        order = tool_get_order(db, order_id)
        trajectory.append(("get_order", order_id))
        if order["status"] != "delivered":
            return trajectory, "Sorry, I can only refund delivered orders."

    tool_refund(db, order_id)
    trajectory.append(("refund", order_id))
    return trajectory, "Your refund is done."


# ---------- tasks ----------

TASKS = [
    {
        "id": "refund-delivered",
        "text": "Please refund order A1.",
        "required_tools": [("get_order", "A1"), ("refund", "A1")],
        "forbidden_tools": ["delete_order"],
        "check_outcome": lambda db: db["orders"]["A1"]["status"] == "refunded"
                                    and db["refunds"] == [{"order": "A1", "amount": 300}],
    },
    {
        "id": "refuse-not-delivered",
        "text": "Please refund order A2.",
        "required_tools": [("get_order", "A2")],
        "forbidden_tools": ["refund", "delete_order"],
        "check_outcome": lambda db: db["orders"]["A2"]["status"] == "shipped"
                                    and db["refunds"] == [],
    },
]


# ---------- graders ----------

def grade_trial(task, trajectory, db):
    names_called = [name for name, _ in trajectory]
    outcome_ok = task["check_outcome"](db)
    required_ok = all(call in trajectory for call in task["required_tools"])
    forbidden_ok = not any(name in task["forbidden_tools"] for name in names_called)
    return {
        "outcome": outcome_ok,
        "tools": required_ok and forbidden_ok,
        "steps": len(trajectory),
        "passed": outcome_ok and required_ok and forbidden_ok,
    }


def run_trials(task, trials, seed):
    rng = random.Random(seed)
    results = []
    for _ in range(trials):
        db = copy.deepcopy(START_DATABASE)      # every trial starts from a clean state
        trajectory, _final_message = mock_agent(task["text"], db, rng)
        results.append(grade_trial(task, trajectory, db))
    return results


def main():
    trials = 200
    for number, task in enumerate(TASKS):
        results = run_trials(task, trials, seed=7 + number)
        pass_rate = sum(r["passed"] for r in results) / trials
        outcome_rate = sum(r["outcome"] for r in results) / trials
        tools_rate = sum(r["tools"] for r in results) / trials
        average_steps = sum(r["steps"] for r in results) / trials
        print(f"Task: {task['id']}")
        print(f"  outcome correct : {outcome_rate:.0%}")
        print(f"  tool use correct: {tools_rate:.0%}")
        print(f"  full pass rate  : {pass_rate:.0%}   (average steps: {average_steps:.1f})")
        for k in (1, 3, 5):
            pass_at_k = 1 - (1 - pass_rate) ** k    # at least one success in k tries
            pass_power_k = pass_rate ** k           # all k tries succeed
            print(f"    k={k}: pass@k={pass_at_k:.0%}   pass^k={pass_power_k:.0%}")
        print()

    print("Read this carefully:")
    print(" * In task 1 the careless agent still gets the right OUTCOME by luck,")
    print("   but the tool check catches that it skipped get_order.")
    print(" * In task 2 the careless agent refunds an order it must not refund.")
    print(" * pass@k goes up with more tries. pass^k goes down.")
    print("   For a support bot, users need it right EVERY time, so pass^k matters more.")


if __name__ == "__main__":
    main()
