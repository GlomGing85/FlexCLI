from __future__ import annotations

import json
import sys

from . import __version__
from .agent import FlexAgent
from .client import MissingAPIKeyError, build_client
from .config import AppConfig, config_path, config_summary, load_config, save_config
from .memory import MemoryStore


HELP_TEXT = """
Команди FlexCLI:
  /help                показати допомогу
  /exit                вийти
  /config              показати поточну конфігурацію
  /mem                 показати останні записи пам'яті
  /reset               очистити коротку історію повідомлень
  /set model <value>   змінити модель
  /set temp <value>    змінити temperature
  /set search on|off   увімк/вимк web search
  /set genskills on|off увімк/вимк generated skills

Усе інше — звичайний чат-запит до агента.
""".strip()


def _print_header(cfg: AppConfig) -> None:
    print(f"FlexCLI v{__version__}")
    print(f"config: {config_path()}")
    print(f"workspace: {cfg.workspace_dir}")
    print("Напиши /help для команд.\n")


def _handle_set(raw: str, cfg: AppConfig) -> bool:
    parts = raw.strip().split(maxsplit=2)
    if len(parts) < 3:
        print("Використання: /set <key> <value>")
        return True
    _, key, value = parts
    if key == "model":
        cfg.model = value
    elif key == "temp":
        cfg.temperature = float(value)
    elif key == "search":
        cfg.web_search_enabled = value.lower() == "on"
    elif key == "genskills":
        cfg.enable_generated_skills = value.lower() == "on"
    else:
        print(f"Невідомий ключ: {key}")
        return True
    save_config(cfg)
    print("Оновлено config:\n" + config_summary(cfg))
    return True


def main() -> None:
    cfg = load_config()
    memory = MemoryStore(cfg.db_path)
    _print_header(cfg)

    try:
        client = build_client(cfg)
    except MissingAPIKeyError as e:
        print(str(e))
        print("Порада: cp .env.example .env && nano .env")
        sys.exit(1)

    agent = FlexAgent(client=client, cfg=cfg, memory=memory)

    while True:
        try:
            user_text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо зустрічі!")
            break

        if not user_text:
            continue
        if user_text == "/exit":
            print("До зустрічі!")
            break
        if user_text == "/help":
            print(HELP_TEXT)
            continue
        if user_text == "/config":
            print(config_summary(cfg))
            continue
        if user_text == "/mem":
            rows = memory.recent_memories(limit=10)
            if not rows:
                print("Пам'ять порожня")
            else:
                for row in rows:
                    print(json.dumps(row, ensure_ascii=False, indent=2))
            continue
        if user_text == "/reset":
            memory.clear_messages()
            print("Коротку історію очищено")
            continue
        if user_text.startswith("/set "):
            _handle_set(user_text, cfg)
            continue

        print("flex> думає...")
        try:
            answer = agent.ask(user_text)
            print(f"flex> {answer}\n")
        except Exception as e:
            print(f"flex> Помилка: {e}\n")
