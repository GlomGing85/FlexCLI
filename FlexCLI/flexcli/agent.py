from __future__ import annotations

import json
from typing import Any

from .config import AppConfig, config_summary
from .memory import MemoryStore
from .skills import ToolContext, execute_tool, tool_specs


class FlexAgent:
    def __init__(self, client: Any, cfg: AppConfig, memory: MemoryStore):
        self.client = client
        self.cfg = cfg
        self.memory = memory
        self.tool_ctx = ToolContext(cfg=cfg, memory=memory)

    def _build_messages(self, user_text: str) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    self.cfg.system_prompt
                    + "\nПоточна конфігурація:\n"
                    + config_summary(self.cfg)
                    + "\nПрацюй у workspace і використовуй інструменти, якщо вони реально допомагають."
                ),
            }
        ]

        related = self.memory.search_memories(user_text, limit=5)
        if related:
            memory_text = "\n\n".join(
                f"id={r['id']} | tags={r['tags']}\n{r['text']}" for r in related
            )
            messages.append(
                {
                    "role": "system",
                    "content": "Релевантна довгострокова пам'ять:\n" + memory_text,
                }
            )

        for row in self.memory.recent_messages(limit=self.cfg.max_history_messages):
            messages.append({"role": row["role"], "content": row["content"]})

        messages.append({"role": "user", "content": user_text})
        return messages

    def ask(self, user_text: str) -> str:
        messages = self._build_messages(user_text)
        tools = tool_specs()

        for _ in range(self.cfg.max_tool_rounds):
            response = self.client.chat.completions.create(
                model=self.cfg.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=self.cfg.temperature,
            )
            msg = response.choices[0].message
            assistant_content = msg.content or ""

            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "content": assistant_content,
            }
            if getattr(msg, "tool_calls", None):
                assistant_message["tool_calls"] = [tc.model_dump() for tc in msg.tool_calls]
            messages.append(assistant_message)

            if getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    try:
                        args = json.loads(tc.function.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    result = execute_tool(tc.function.name, args, self.tool_ctx)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": result,
                        }
                    )
                continue

            final = assistant_content.strip() or "(порожня відповідь)"
            self.memory.save_message("user", user_text)
            self.memory.save_message("assistant", final)
            return final

        fallback = (
            "Я виконав забагато кроків з інструментами підряд і зупинився. "
            "Спробуй уточнити запит або зменшити задачу."
        )
        self.memory.save_message("user", user_text)
        self.memory.save_message("assistant", fallback)
        return fallback
