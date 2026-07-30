"""One chat interface over Kimi (Moonshot) and Claude.

Standard library only — no pip install needed to run the generators. Moonshot
exposes an OpenAI-compatible /chat/completions endpoint, so the two providers
differ only in URL, auth header and response shape.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from . import config

TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class Reply:
    text: str
    model: str
    provider: str


class LLMError(RuntimeError):
    pass


def _post(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    for key, value in {**headers, "Content-Type": "application/json"}.items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:400]
        raise LLMError(f"{exc.code} from {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMError(
            f"could not reach {url}: {exc.reason}. If you are running this "
            "inside a sandbox, outbound network is probably blocked — run it "
            "on your own machine."
        ) from exc


def _kimi(system: str, prompt: str, temperature: float) -> Reply:
    key = config.require(
        "MOONSHOT_API_KEY",
        "Get one at https://platform.moonshot.ai/ then put it in .env "
        "(copy .env.example). Never commit it.",
    )
    base = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.ai/v1").rstrip("/")
    model = os.environ.get("MOONSHOT_MODEL", "kimi-k2-0905-preview")
    data = _post(
        f"{base}/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        },
    )
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise LLMError(f"unexpected Moonshot response shape: {str(data)[:300]}") from exc
    return Reply(text=text, model=model, provider="kimi")


def _claude(system: str, prompt: str, temperature: float) -> Reply:
    key = config.require(
        "ANTHROPIC_API_KEY",
        "Get one at https://console.anthropic.com/ then put it in .env.",
    )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    data = _post(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01"},
        {
            "model": model,
            "max_tokens": 4096,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    try:
        text = "".join(
            block["text"] for block in data["content"] if block.get("type") == "text"
        )
    except (KeyError, TypeError) as exc:
        raise LLMError(f"unexpected Anthropic response shape: {str(data)[:300]}") from exc
    return Reply(text=text, model=model, provider="claude")


def chat(system: str, prompt: str, *, temperature: float = 0.8) -> Reply:
    """Send one turn to the configured provider."""
    config.load_dotenv()
    name = config.provider()
    if name == "kimi":
        return _kimi(system, prompt, temperature)
    if name == "claude":
        return _claude(system, prompt, temperature)
    raise LLMError(f"unknown FEHU_PROVIDER={name!r} — expected 'kimi' or 'claude'")


def extract_json_array(text: str) -> list[Any]:
    """Pull the first JSON array out of a reply, tolerating prose or fences."""
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise LLMError(f"no JSON array found in reply: {text[:300]}")
    return json.loads(text[start : end + 1])
