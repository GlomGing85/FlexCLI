# FlexCLI

**FlexCLI** — это терминальный AI-ассистент для **Android + Termux**, ориентированный на:
- общение
- помощь с кодом
- работу с файлами и папками
- web search
- память
- создание заготовок для новых скиллов

Язык: [English](README.md) | [Українська](README.ua.md) | **Русский**

> Текущий релиз: **1.0.0-alpha.3**

## Статус проекта
FlexCLI сейчас находится на стадии **alpha / MVP**.
Он уже работает как локальный CLI-агент, но пока не готов для production-использования.

На данный момент:
- документация доступна на нескольких языках
- сам интерфейс CLI пока в основном на украинском
- выбор языка интерфейса планируется в будущих релизах

## Возможности

### Core
- интерактивный CLI-чат
- интеграция с NVIDIA API через OpenAI-compatible endpoint
- агентный цикл с tool/function calling
- JSON-конфиг
- workspace sandbox
- память на SQLite

### Встроенные инструменты
- `list_files`
- `read_file`
- `write_file`
- `edit_file`
- `mkdir`
- `web_search`
- `save_memory`
- `search_memory`
- `create_skill`

### Текущие команды CLI
- `/help`
- `/config`
- `/mem`
- `/reset`
- `/set model <value>`
- `/set temp <value>`
- `/set search on|off`
- `/set genskills on|off`
- `/exit`

## Структура репозитория

```text
FlexCLI/
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ RELEASE.md
├─ README.md
├─ README.ua.md
├─ README.ru.md
├─ install-termux.sh
├─ update-termux.sh
├─ run.sh
├─ pyproject.toml
├─ requirements.txt
├─ .github/
│  ├─ workflows/python-ci.yml
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ ISSUE_TEMPLATE/
│     ├─ bug_report.md
│     └─ feature_request.md
└─ flexcli/
   ├─ __init__.py
   ├─ __main__.py
   ├─ agent.py
   ├─ cli.py
   ├─ client.py
   ├─ config.py
   ├─ memory.py
   └─ skills.py
```

После первого запуска FlexCLI создаёт:

```text
~/.flexcli/
├─ .env
├─ config.json
├─ memory.db
├─ generated_skills/
└─ workspace/
```

## Требования
- Android-устройство
- [Termux](https://termux.dev/)
- Python в Termux
- NVIDIA API key (`nvapi-...`)

## Установка в Termux

### 1. Клонирование репозитория
```bash
pkg update
pkg install git -y
git clone https://github.com/GlomGing85/FlexCLI.git
cd FlexCLI
```

### 2. Запуск установщика
```bash
bash install-termux.sh
```

### 3. Добавление NVIDIA API ключа
```bash
nano ~/.flexcli/.env
```

Вставь:
```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Запуск FlexCLI
```bash
flexcli
```

## Обновление
Если FlexCLI установлен из GitHub:

```bash
cd ~/FlexCLI
bash update-termux.sh
```

## Конфигурация
Основной конфиг:

```bash
~/.flexcli/config.json
```

Пример:

```json
{
  "base_url": "https://integrate.api.nvidia.com/v1",
  "model": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
  "temperature": 0.3,
  "max_tool_rounds": 5,
  "max_history_messages": 12,
  "web_search_enabled": true,
  "confirm_destructive": true,
  "enable_generated_skills": false,
  "workspace_dir": "/data/data/com.termux/files/home/.flexcli/workspace",
  "db_path": "/data/data/com.termux/files/home/.flexcli/memory.db",
  "system_prompt": "Ты — FlexCLI..."
}
```

### Где хранить API ключ
FlexCLI может читать `.env` из:
- `~/.flexcli/.env`
- `.env` в корне репозитория
- `.env` в текущей папке запуска

Рекомендуемый вариант для Termux:

```bash
~/.flexcli/.env
```

## Модель памяти
Сейчас FlexCLI использует два простых уровня памяти:

### Краткосрочная память
Последняя история диалога в SQLite.

### Долгосрочная память
Отдельно сохранённые полезные предпочтения и заметки.

Что полезно сохранять:
- любимый язык программирования
- предпочитаемый стиль ответов
- названия проектов
- важные пути
- долгосрочные задачи

## Генерация скиллов
Инструмент `create_skill` сейчас создаёт Python-заготовку в:

```bash
~/.flexcli/generated_skills/
```

Так сделано специально.
Сгенерированные скиллы создаются безопасно и **не выполняются автоматически по умолчанию**.

## Roadmap

### Alpha / MVP
- чат
- файловые инструменты
- память
- web search
- конфиг
- заготовки для скиллов

### Следующие шаги
- streaming output
- `/mode chat|code|research`
- append/delete инструменты с подтверждением
- более безопасное выполнение кода
- автозагрузка generated skills
- лучший поиск и сводки
- выбор языка CLI

## Участие в проекте
См. [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия
MIT — см. [LICENSE](LICENSE).
