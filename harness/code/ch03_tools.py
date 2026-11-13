"""
Chapter 3 - Tools: descriptions, argument checks, helpful errors, short results.

Run:  python ch03_tools.py

The model never runs code. It only writes a request such as
    {"tool": "search_orders", "args": {"customer": "asha"}}
The harness checks the request, runs the function and sends back text.

Four things a good harness does for every tool call:
  1. shows the model a clear description of each tool (the "schema")
  2. checks the arguments before running anything
  3. turns errors into messages the model can act on
  4. keeps results short, so they do not fill the context

No key needed. Standard library only.
"""

import json

ORDERS = [{"id": f"A{n}", "customer": "asha" if n % 2 else "ravi", "item": f"item-{n}", "price": 100 * n}
          for n in range(1, 41)]


def search_orders(customer, limit=5):
    found = [o for o in ORDERS if o["customer"] == customer]
    return found[:limit], len(found)


def get_order(order_id):
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    raise LookupError(f"No order with id '{order_id}'. Ids look like A1, A2 ... A40. "
                      "Use search_orders to find ids for a customer.")


# The schema is what the MODEL reads. Write it like a note to a new team member.
TOOL_SPECS = {
    "search_orders": {
        "function": search_orders,
        "description": "Find orders of one customer. Returns the first `limit` orders and the total count. "
                       "Use this first when you do not know the order id.",
        "params": {
            "customer": {"type": str, "required": True, "help": "customer name in lower case, e.g. 'asha'"},
            "limit": {"type": int, "required": False, "help": "max orders to return, 1 to 10 (default 5)"},
        },
    },
    "get_order": {
        "function": get_order,
        "description": "Get all details of one order by its id.",
        "params": {
            "order_id": {"type": str, "required": True, "help": "order id such as 'A7'"},
        },
    },
}

MAX_RESULT_CHARS = 300


def describe_tools():
    """The text that goes into the prompt so the model knows its tools."""
    lines = []
    for name, spec in TOOL_SPECS.items():
        lines.append(f"- {name}: {spec['description']}")
        for param, rule in spec["params"].items():
            need = "required" if rule["required"] else "optional"
            lines.append(f"    {param} ({rule['type'].__name__}, {need}): {rule['help']}")
    return "\n".join(lines)


def call_tool(name, args):
    """Check, run, and always return a string for the model. Never crash the loop."""
    if name not in TOOL_SPECS:
        return f"ERROR: unknown tool '{name}'. Available tools: {', '.join(TOOL_SPECS)}."
    spec = TOOL_SPECS[name]

    for param, rule in spec["params"].items():
        if rule["required"] and param not in args:
            return f"ERROR: missing argument '{param}' ({rule['help']})."
    for param, value in args.items():
        if param not in spec["params"]:
            return f"ERROR: unknown argument '{param}'. Allowed: {', '.join(spec['params'])}."
        expected = spec["params"][param]["type"]
        if not isinstance(value, expected):
            return f"ERROR: '{param}' must be {expected.__name__}, got {type(value).__name__}."
    if name == "search_orders" and not 1 <= args.get("limit", 5) <= 10:
        return "ERROR: 'limit' must be between 1 and 10."

    try:
        result = spec["function"](**args)
    except LookupError as error:
        return "ERROR: " + str(error)

    if name == "search_orders":
        orders, total = result
        text = json.dumps(orders)
        if total > len(orders):
            text += f"\n(showing {len(orders)} of {total}. Ask for a specific order with get_order.)"
    else:
        text = json.dumps(result)
    if len(text) > MAX_RESULT_CHARS:
        text = text[:MAX_RESULT_CHARS] + f"... [cut: result had {len(text)} characters]"
    return text


def main():
    print("WHAT THE MODEL SEES ABOUT ITS TOOLS")
    print(describe_tools())
    print()
    calls = [
        ("search_orders", {"customer": "asha", "limit": 2}),
        ("get_order", {"order_id": "A7"}),
        ("get_order", {"order_id": "7"}),                 # wrong id format
        ("get_order", {}),                                # missing argument
        ("search_orders", {"customer": "asha", "limit": "many"}),   # wrong type
        ("delete_order", {"order_id": "A7"}),             # tool does not exist
        ("search_orders", {"customer": "asha", "limit": 10}),       # long result gets cut
    ]
    for name, args in calls:
        print(f"CALL   {name}({args})")
        print(f"RESULT {call_tool(name, args)}")
        print()
    print("Every error tells the model what to do next. A bare 'KeyError' would not.")


if __name__ == "__main__":
    main()
