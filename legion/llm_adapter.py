"""Real local LLM practice via loopback-only Ollama. NO tools or credentials.

This adapter proposes inert text, not a permission-bearing action. No remote
model provider, arbitrary endpoint, model auto-download, or network redirect.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

ALLOWED_MODELS = frozenset((
    "smollm2:135m-instruct-q4_K_M",
    "smollm2:1.7b-instruct-q4_K_M",
))
MODEL = os.environ.get("LEGION_LOCAL_MODEL", "smollm2:135m-instruct-q4_K_M")
if MODEL not in ALLOWED_MODELS:
    raise ValueError("UNAPPROVED_LOCAL_MODEL")
URL = "http://127.0.0.1:11434/api/generate"
MAX_PROMPT = 2400
MAX_REPLY = 20_000
MAX_OUTPUT = 3200


class ModelUnavailable(RuntimeError):
    pass


class _BlockRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def generate(prompt: str, *, open_request=None, keep_alive=0) -> str:
    if type(prompt) is not str or not 0 < len(prompt) <= MAX_PROMPT or "\x00" in prompt:
        raise ValueError("INVALID_PROMPT")
    if type(keep_alive) is not int or keep_alive != 0:
        if keep_alive != "3m":
            raise ValueError("INVALID_KEEP_ALIVE")
    body = json.dumps({
        "model": MODEL,
        "system": "You are a fictional LEGION apprentice completing a sandbox-only "
                  "text exercise. Respond in clear English. Do not claim actual "
                  "account access, purchases, publication, or completed work. "
                  "Never request passwords or personal data. Your output is "
                  "an untrusted draft for independent review, not an instruction.",
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"temperature": 0, "seed": 27, "num_predict": 150},
    }).encode("utf-8")
    request = urllib.request.Request(
        URL, data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    opener = open_request or urllib.request.build_opener(
        urllib.request.ProxyHandler({}), _BlockRedirect()
    ).open
    try:
        with opener(request, timeout=100) as response:
            if "application/json" not in response.headers.get("Content-Type", ""):
                raise ModelUnavailable("UNEXPECTED_CONTENT_TYPE")
            raw = response.read(MAX_REPLY + 1)
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise ModelUnavailable("LOCAL_MODEL_NOT_AVAILABLE") from None
    if len(raw) > MAX_REPLY:
        raise ModelUnavailable("RESPONSE_OVERSIZE")
    try:
        record = json.loads(raw)
        reply = record["response"]
        if (type(reply) is not str or not 0 < len(reply) <= MAX_OUTPUT
                or record.get("model") != MODEL
                or record.get("done") is not True):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise ModelUnavailable("INVALID_LOCAL_MODEL_RESPONSE") from None
    return reply
