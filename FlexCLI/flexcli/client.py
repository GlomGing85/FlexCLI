from __future__ import annotations

import os

from openai import OpenAI

from .config import AppConfig


class MissingAPIKeyError(RuntimeError):
    pass


def build_client(cfg: AppConfig) -> OpenAI:
    api_key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "Не знайдено NVIDIA_API_KEY. Скопіюй .env.example в .env і встав свій nvapi- ключ."
        )
    return OpenAI(base_url=cfg.base_url, api_key=api_key)
