from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import AppConfig


class MissingAPIKeyError(RuntimeError):
    pass


class APIRequestError(RuntimeError):
    pass


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | dict | None = None,
        temperature: float = 0.3,
    ) -> dict:
        payload: dict = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice

        data = json.dumps(payload).encode("utf-8")
        req = Request(
            self.base_url + "/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "FlexCLI/1.0",
            },
            method="POST",
        )

        try:
            with urlopen(req, timeout=120) as resp:
                body = resp.read().decode("utf-8")
        except HTTPError as e:
            detail = e.read().decode("utf-8", "ignore") if hasattr(e, "read") else str(e)
            raise APIRequestError(f"HTTP {e.code}: {detail}") from e
        except URLError as e:
            raise APIRequestError(f"Мережева помилка: {e}") from e

        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            raise APIRequestError(f"Некоректна JSON-відповідь від API: {body[:500]}") from e


def build_client(cfg: AppConfig) -> OpenAICompatibleClient:
    api_key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "Не знайдено NVIDIA_API_KEY. Відкрий ~/.flexcli/.env і встав свій nvapi- ключ."
        )
    return OpenAICompatibleClient(base_url=cfg.base_url, api_key=api_key)
