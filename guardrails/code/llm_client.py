"""
llm_client.py - one small helper used by the examples.

What it does:
  * If the environment variable OPENROUTER_API_KEY is set, it calls a free
    model on OpenRouter (https://openrouter.ai).
  * If the key is NOT set, or the call fails, it uses a "mock" function
    instead. A mock is a fake model: normal Python code that returns an answer.

So every example in this handbook runs with no key and no internet.

It uses only the Python standard library. Nothing to install.
"""

import json
import os
import urllib.error
import urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# "openrouter/free" lets OpenRouter pick a free model for you.
# Free model names change often. You can set your own with OPENROUTER_MODEL.
DEFAULT_MODEL = "openrouter/free"

_printed_notes = set()


def _note(text):
    """Print a short note only once."""
    if text not in _printed_notes:
        _printed_notes.add(text)
        print("[llm_client] " + text)


def has_key():
    """True if a key is set in the environment."""
    return bool(os.environ.get("OPENROUTER_API_KEY", "").strip())


def ask_llm(prompt, system=None, mock=None, max_tokens=300, temperature=0.0):
    """
    Send a prompt to a model and return the answer as a string.

    prompt      : the user message.
    system      : optional system message (the rules for the model).
    mock        : a function mock(prompt) -> str. Used when there is no key
                  or when the real call fails.
    max_tokens  : upper limit for the answer length.
    temperature : 0.0 gives the most stable answers. Good for evals.
    """
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()

    if not key:
        _note("No OPENROUTER_API_KEY found. Using the mock model.")
        return _run_mock(mock, prompt)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL),
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        if not text:
            raise ValueError("the model returned an empty answer")
        _note("Using a real model: " + str(data.get("model", body["model"])))
        return text.strip()
    except (urllib.error.URLError, KeyError, IndexError, ValueError, TimeoutError, OSError) as error:
        # Free models have small daily limits. If anything goes wrong,
        # we do not crash. We fall back to the mock.
        _note("Real call failed (" + type(error).__name__ + "). Using the mock model.")
        return _run_mock(mock, prompt)


def _run_mock(mock, prompt):
    if mock is None:
        return "MOCK ANSWER: no mock function was given."
    return mock(prompt)


if __name__ == "__main__":
    # Small self-test. Run:  python llm_client.py
    def echo_mock(prompt):
        return "mock says: you asked '" + prompt + "'"

    print("Key found:", has_key())
    print(ask_llm("Say hello in three words.", mock=echo_mock))
