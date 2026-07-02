from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from duckduckgo_search import DDGS

from .config import AppConfig, flexcli_home
from .memory import MemoryStore


class ToolContext:
    def __init__(self, cfg: AppConfig, memory: MemoryStore):
        self.cfg = cfg
        self.memory = memory
        self.workspace = Path(cfg.workspace_dir).expanduser().resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def resolve_workspace_path(self, path: str) -> Path:
        raw = Path(path)
        target = (self.workspace / raw).resolve() if not raw.is_absolute() else raw.resolve()
        workspace_str = str(self.workspace)
        target_str = str(target)
        if target_str != workspace_str and not target_str.startswith(workspace_str + "/"):
            raise ValueError(f"Шлях поза workspace заборонений: {path}")
        return target


def tool_specs() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "Показати список файлів і папок у workspace або в підпапці.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Відносний шлях у workspace, напр. . або src"}
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Прочитати текстовий файл із workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Відносний шлях до файлу"}
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Створити або повністю перезаписати файл у workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": "Замінити шматок тексту у файлі. Якщо old_text не знайдено — повернути помилку.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "old_text": {"type": "string"},
                        "new_text": {"type": "string"}
                    },
                    "required": ["path", "old_text", "new_text"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "mkdir",
                "description": "Створити папку у workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Пошук у вебі за запитом і коротке повернення результатів.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "max_results": {"type": "integer", "minimum": 1, "maximum": 10}
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "save_memory",
                "description": "Зберегти довгострокову пам'ять про вподобання, факт чи домовленість.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "tags": {"type": "string"}
                    },
                    "required": ["text"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_memory",
                "description": "Знайти релевантні записи з довгострокової пам'яті.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 20}
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_skill",
                "description": "Створити новий Python-скіл як файл. Безпечніше створювати шаблон або код-заготовку, а не довільний небезпечний код.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "parameters_json": {"type": "string", "description": "JSON-схема параметрів у вигляді рядка"},
                        "python_code": {"type": "string", "description": "Повний код файла або порожньо для шаблона"}
                    },
                    "required": ["name", "description"],
                },
            },
        },
    ]


def execute_tool(name: str, args: dict[str, Any], ctx: ToolContext) -> str:
    handlers = {
        "list_files": _list_files,
        "read_file": _read_file,
        "write_file": _write_file,
        "edit_file": _edit_file,
        "mkdir": _mkdir,
        "web_search": _web_search,
        "save_memory": _save_memory,
        "search_memory": _search_memory,
        "create_skill": _create_skill,
    }
    if name not in handlers:
        return f"Невідомий інструмент: {name}"
    try:
        return handlers[name](ctx, **args)
    except Exception as e:
        return f"Помилка інструмента {name}: {e}"


def _list_files(ctx: ToolContext, path: str = ".") -> str:
    target = ctx.resolve_workspace_path(path)
    if not target.exists():
        return f"Шлях не існує: {path}"
    if target.is_file():
        return f"Це файл: {target.relative_to(ctx.workspace)}"
    items = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    lines = []
    for item in items[:200]:
        rel = item.relative_to(ctx.workspace)
        kind = "DIR " if item.is_dir() else "FILE"
        lines.append(f"{kind} {rel}")
    if not lines:
        return f"Папка порожня: {path}"
    return "\n".join(lines)


def _read_file(ctx: ToolContext, path: str) -> str:
    target = ctx.resolve_workspace_path(path)
    if not target.exists():
        return f"Файл не знайдено: {path}"
    if not target.is_file():
        return f"Шлях не є файлом: {path}"
    data = target.read_text(encoding="utf-8")
    if len(data) > 20000:
        data = data[:20000] + "\n\n[...обрізано...]"
    return data


def _write_file(ctx: ToolContext, path: str, content: str) -> str:
    target = ctx.resolve_workspace_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Файл збережено: {target.relative_to(ctx.workspace)} ({len(content)} символів)"


def _edit_file(ctx: ToolContext, path: str, old_text: str, new_text: str) -> str:
    target = ctx.resolve_workspace_path(path)
    if not target.exists() or not target.is_file():
        return f"Файл не знайдено: {path}"
    data = target.read_text(encoding="utf-8")
    if old_text not in data:
        return "old_text не знайдено у файлі"
    updated = data.replace(old_text, new_text, 1)
    target.write_text(updated, encoding="utf-8")
    return f"Файл оновлено: {target.relative_to(ctx.workspace)}"


def _mkdir(ctx: ToolContext, path: str) -> str:
    target = ctx.resolve_workspace_path(path)
    target.mkdir(parents=True, exist_ok=True)
    return f"Папку створено: {target.relative_to(ctx.workspace)}"


def _web_search(ctx: ToolContext, query: str, max_results: int = 5) -> str:
    if not ctx.cfg.web_search_enabled:
        return "Web search вимкнений у config.json"
    results: list[str] = []
    with DDGS() as ddgs:
        for idx, item in enumerate(ddgs.text(query, max_results=max_results), start=1):
            title = item.get("title", "(без назви)")
            href = item.get("href", "")
            body = item.get("body", "")
            results.append(f"{idx}. {title}\nURL: {href}\n{body}")
    if not results:
        return f"Нічого не знайдено за запитом: {query}"
    return "\n\n".join(results)


def _save_memory(ctx: ToolContext, text: str, tags: str = "") -> str:
    row_id = ctx.memory.add_memory(text=text, tags=tags)
    return f"Пам'ять збережено. id={row_id}"


def _search_memory(ctx: ToolContext, query: str, limit: int = 5) -> str:
    rows = ctx.memory.search_memories(query=query, limit=limit)
    if not rows:
        return f"Нічого не знайдено в пам'яті за запитом: {query}"
    return "\n\n".join(
        f"id={r['id']} | tags={r['tags']}\n{r['text']}" for r in rows
    )


def _safe_skill_name(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip()).strip("_").lower()
    if not slug:
        raise ValueError("Некоректна назва скіла")
    return slug


def _create_skill(
    ctx: ToolContext,
    name: str,
    description: str,
    parameters_json: str = "",
    python_code: str = "",
) -> str:
    slug = _safe_skill_name(name)
    skill_dir = flexcli_home() / "generated_skills"
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / f"{slug}.py"

    if not python_code.strip():
        if parameters_json.strip():
            parsed = json.loads(parameters_json)
        else:
            parsed = {
                "type": "object",
                "properties": {
                    "example": {"type": "string", "description": "Приклад параметра"}
                },
                "required": [],
            }
        schema_text = repr(parsed)
        python_code = f'''"""Автоматично згенерований FlexCLI скіл.
Назва: {name}
Опис: {description}

Що далі:
1. Відредагуй цей файл.
2. Реалізуй функцію run(...).
3. Додай автозавантаження generated_skills у наступній версії FlexCLI.
"""

TOOL_NAME = "{slug}"
TOOL_DESCRIPTION = {description!r}
TOOL_PARAMETERS = {schema_text}


def run(**kwargs):
    return {{
        "status": "todo",
        "tool": TOOL_NAME,
        "received": kwargs,
        "message": "Реалізуй логіку цього скіла у файлі generated_skills/{slug}.py"
    }}
'''

    path.write_text(python_code, encoding="utf-8")
    return (
        f"Скіл створено: {path}\n"
        f"Автозавантаження generated skills зараз {'УВІМКНЕНО' if ctx.cfg.enable_generated_skills else 'ВИМКНЕНО'}.")
