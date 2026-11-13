"""
Chapter 7 - Permissions and a simple sandbox.

Run:  python ch07_permissions.py

The harness decides what the model is ALLOWED to do. Two layers:

  1. Sandbox   - hard limits enforced by code. Here: file tools can only touch
                 one workspace folder, and only a few commands are allowed.
  2. Permission mode - when to ask the human:
       "read-only" : only reading tools run
       "ask"       : writing needs a yes from the human
       "auto"      : everything inside the sandbox runs

The sandbox here is a teaching version. A real one uses the operating system
(containers, or tools like bubblewrap on Linux) and also limits the network.

No key needed. Standard library only. It only writes inside a temporary folder.
"""

import os
import tempfile

READ_TOOLS = {"read_file", "list_files"}
WRITE_TOOLS = {"write_file", "run_command"}
ALLOWED_COMMANDS = {"run_tests", "format_code"}       # an allow list, not a block list


class Sandbox:
    def __init__(self, workspace):
        self.workspace = os.path.realpath(workspace)

    def safe_path(self, relative_path):
        """Turn a path from the model into a real path, and refuse anything outside the workspace."""
        full = os.path.realpath(os.path.join(self.workspace, relative_path))
        if os.path.commonpath([full, self.workspace]) != self.workspace:
            raise PermissionError(f"'{relative_path}' is outside the workspace")
        return full

    def read_file(self, path):
        with open(self.safe_path(path), encoding="utf-8") as file:
            return file.read()

    def write_file(self, path, text):
        with open(self.safe_path(path), "w", encoding="utf-8") as file:
            file.write(text)
        return f"wrote {len(text)} characters to {path}"

    def list_files(self):
        return ", ".join(sorted(os.listdir(self.workspace)))

    def run_command(self, command):
        if command not in ALLOWED_COMMANDS:
            raise PermissionError(f"command '{command}' is not on the allow list {sorted(ALLOWED_COMMANDS)}")
        return f"(pretend) ran {command}: ok"


def execute(sandbox, mode, tool, args, approver):
    """The permission gate. Returns a text result for the model."""
    if tool not in READ_TOOLS | WRITE_TOOLS:
        return "DENIED: unknown tool"
    if tool in WRITE_TOOLS:
        if mode == "read-only":
            return "DENIED: read-only mode"
        if mode == "ask" and not approver(tool, args):
            return "DENIED: the user said no"
    try:
        return "OK: " + str(getattr(sandbox, tool)(**args))
    except PermissionError as error:
        return "BLOCKED BY SANDBOX: " + str(error)
    except FileNotFoundError:
        return "ERROR: file not found. Use list_files to see what exists."


def scripted_user(tool, args):
    """A fake human: says yes to writing notes.txt, no to everything else."""
    return tool == "write_file" and args.get("path") == "notes.txt"


CALLS = [
    ("list_files", {}),
    ("read_file", {"path": "notes.txt"}),
    ("write_file", {"path": "notes.txt", "text": "updated by the agent"}),
    ("write_file", {"path": "report.txt", "text": "new file"}),
    ("read_file", {"path": "../secret.txt"}),                  # tries to leave the workspace
    ("write_file", {"path": "../../evil.txt", "text": "x"}),   # tries to leave the workspace
    ("run_command", {"command": "run_tests"}),
    ("run_command", {"command": "delete_everything"}),         # not on the allow list
]


def main():
    for mode in ("read-only", "ask", "auto"):
        workspace = tempfile.mkdtemp()
        with open(os.path.join(workspace, "notes.txt"), "w", encoding="utf-8") as file:
            file.write("hello")
        sandbox = Sandbox(workspace)
        print(f"MODE: {mode}")
        for tool, args in CALLS:
            shown = ", ".join(f"{k}={v!r}" for k, v in args.items())
            print(f"  {tool}({shown})")
            print(f"      -> {execute(sandbox, mode, tool, args, scripted_user)}")
        print()
    print("Notice: even in 'auto' mode, the sandbox still blocks paths outside the workspace")
    print("and commands that are not on the allow list. Modes can be relaxed. Hard limits stay.")


if __name__ == "__main__":
    main()
