from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_SYSTEM_PROMPT = """Ти — FlexCLI, корисний CLI агент для телефону.
Твоя спеціалізація: спілкування, код, робота з файлами, пошук, пам'ять і створення нових скілів.
Правила:
1. Будь коротким, але корисним.
2. Якщо для задачі потрібен інструмент — використовуй його.
3. Працюй лише в межах workspace, якщо користувач явно не просить інше.
4. Перед ризикованими діями або перезаписом важливих файлів спочатку попередь.
5. Якщо створюєш новий скіл — зроби це безпечно і поясни, як його активувати.
6. Пам'ятай важливі вподобання користувача, якщо вони можуть знадобитись пізніше.
"""


@dataclass
class AppConfig:
    base_url: str = "https://integrate.api.nvidia.com/v1"
    model: str = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
    temperature: float = 0.3
    max_tool_rounds: int = 5
    max_history_messages: int = 12
    web_search_enabled: bool = True
    confirm_destructive: bool = True
    enable_generated_skills: bool = False
    workspace_dir: str = ""
    db_path: str = ""
    system_prompt: str = DEFAULT_SYSTEM_PROMPT


def flexcli_home() -> Path:
    raw = os.environ.get("FLEXCLI_HOME")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".flexcli"


def config_path() -> Path:
    return flexcli_home() / "config.json"


def default_workspace_dir() -> str:
    return str((flexcli_home() / "workspace").expanduser())


def default_db_path() -> str:
    return str((flexcli_home() / "memory.db").expanduser())


def ensure_dirs() -> None:
    home = flexcli_home()
    home.mkdir(parents=True, exist_ok=True)
    (home / "workspace").mkdir(parents=True, exist_ok=True)
    (home / "generated_skills").mkdir(parents=True, exist_ok=True)


def _normalized_config(data: dict) -> AppConfig:
    cfg = AppConfig(**data)
    if not cfg.workspace_dir:
        cfg.workspace_dir = default_workspace_dir()
    if not cfg.db_path:
        cfg.db_path = default_db_path()
    return cfg


def load_env_files() -> None:
    ensure_dirs()
    home_env = flexcli_home() / ".env"
    repo_env = Path(__file__).resolve().parent.parent / ".env"
    cwd_env = Path.cwd() / ".env"

    if home_env.exists():
        load_dotenv(home_env)
    if repo_env.exists():
        load_dotenv(repo_env)
    if cwd_env.exists():
        load_dotenv(cwd_env)


def load_config() -> AppConfig:
    load_env_files()
    ensure_dirs()
    path = config_path()

    if not path.exists():
        cfg = _normalized_config({})
        save_config(cfg)
        return cfg

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return _normalized_config(data)


def save_config(cfg: AppConfig) -> None:
    ensure_dirs()
    path = config_path()
    data = asdict(cfg)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def config_summary(cfg: AppConfig) -> str:
    return (
        f"model={cfg.model}\n"
        f"base_url={cfg.base_url}\n"
        f"workspace_dir={cfg.workspace_dir}\n"
        f"db_path={cfg.db_path}\n"
        f"web_search_enabled={cfg.web_search_enabled}\n"
        f"enable_generated_skills={cfg.enable_generated_skills}\n"
        f"confirm_destructive={cfg.confirm_destructive}"
    )
