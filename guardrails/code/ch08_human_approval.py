"""
Chapter 8 - Human-in-the-loop: ask a person before risky actions.

Run:  python ch08_human_approval.py                (uses a scripted "human", no typing needed)
      python ch08_human_approval.py --interactive  (you type y or n yourself)

Every tool gets a risk level:
  low    -> run automatically         (reading data)
  medium -> run and write to the log  (small changes that are easy to undo)
  high   -> ask a human first         (money, deleting, sending messages)
  banned -> never run

The model only PROPOSES a tool call. Our code decides if it runs.

No key needed. Standard library only.
"""

import sys

TOOL_RISK = {
    "get_order": "low",
    "add_note": "medium",
    "refund": "high",
    "send_email": "high",
    "delete_account": "banned",
}

REFUND_AUTO_LIMIT = 200     # small refunds are fine without a human

audit_log = []


def risk_of(tool, arguments):
    """Risk can depend on the arguments, not only on the tool name."""
    risk = TOOL_RISK.get(tool, "banned")        # unknown tool = banned (deny by default)
    if tool == "refund" and arguments.get("amount", 0) <= REFUND_AUTO_LIMIT:
        risk = "medium"
    return risk


def run_tool(tool, arguments):
    """Stand-in for the real tools."""
    return f"{tool} done with {arguments}"


def scripted_approver(tool, arguments):
    """A fake human for the demo: approves refunds up to 1000, refuses the rest."""
    return tool == "refund" and arguments.get("amount", 0) <= 1000


def console_approver(tool, arguments):
    """A real human at the keyboard."""
    print(f"    APPROVAL NEEDED: {tool} {arguments}")
    return input("    Approve? (y/n): ").strip().lower() == "y"


def execute(tool, arguments, approver):
    risk = risk_of(tool, arguments)

    if risk == "banned":
        decision, result = "denied (banned tool)", None
    elif risk == "high":
        if approver(tool, arguments):
            decision, result = "approved by human", run_tool(tool, arguments)
        else:
            decision, result = "rejected by human", None
    else:
        decision, result = "auto (" + risk + " risk)", run_tool(tool, arguments)

    # Write everything down. A log lets you study what happened later.
    audit_log.append({"tool": tool, "arguments": arguments, "risk": risk, "decision": decision})
    return decision, result


# Tool calls that the model "proposed" in one conversation.
PROPOSED_CALLS = [
    ("get_order", {"order_id": "A1"}),
    ("add_note", {"order_id": "A1", "text": "customer called"}),
    ("refund", {"order_id": "A1", "amount": 150}),
    ("refund", {"order_id": "A2", "amount": 900}),
    ("refund", {"order_id": "A3", "amount": 50000}),
    ("send_email", {"to": "all-customers", "text": "Big sale!"}),
    ("delete_account", {"user": "asha"}),
    ("launch_rocket", {}),
]


def main():
    approver = console_approver if "--interactive" in sys.argv else scripted_approver
    for tool, arguments in PROPOSED_CALLS:
        decision, result = execute(tool, arguments, approver)
        print(f"{tool:15} {str(arguments):45} -> {decision}")

    print()
    print("AUDIT LOG")
    for entry in audit_log:
        print(f"  risk={entry['risk']:6} decision={entry['decision']:22} tool={entry['tool']}")

    asked = sum(1 for e in audit_log if e["risk"] == "high")
    print()
    print(f"The human was asked {asked} times out of {len(audit_log)} calls.")
    print("Ask too often and people click 'yes' without reading. Keep approvals for what matters.")


if __name__ == "__main__":
    main()
