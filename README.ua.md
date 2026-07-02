# FlexCLI

**FlexCLI** — це термінальний AI-асистент для **Android + Termux**, заточений під:
- спілкування
- допомогу з кодом
- роботу з файлами та папками
- web search
- пам'ять
- створення заготовок для нових скілів

Мова: [English](README.md) | **Українська** | [Русский](README.ru.md)

> Поточний реліз: **1.0.0-alpha.2**

## Стан проєкту
FlexCLI зараз у стадії **alpha / MVP**.
Він уже працює як локальний CLI-агент, але ще не є production-ready.

На даний момент:
- документація доступна кількома мовами
- сам CLI-процес поки що переважно українською
- вибір мови інтерфейсу планується в майбутніх релізах

## Можливості

### Core
- інтерактивний CLI чат
- інтеграція з NVIDIA API через OpenAI-compatible endpoint
- агентний цикл з tool/function calling
- JSON-конфіг
- workspace sandbox
- пам'ять на SQLite

### Вбудовані інструменти
- `list_files`
- `read_file`
- `write_file`
- `edit_file`
- `mkdir`
- `web_search`
- `save_memory`
- `search_memory`
- `create_skill`

### Поточні команди CLI
- `/help`
- `/config`
- `/mem`
- `/reset`
- `/set model <value>`
- `/set temp <value>`
- `/set search on|off`
- `/set genskills on|off`
- `/exit`

## Структура репозиторію

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

Після першого запуску FlexCLI створює:

```text
~/.flexcli/
├─ .env
├─ config.json
├─ memory.db
├─ generated_skills/
└─ workspace/
```

## Вимоги
- Android-пристрій
- [Termux](https://termux.dev/)
- Python у Termux
- NVIDIA API key (`nvapi-...`)

## Встановлення в Termux

### 1. Клонування репозиторію
```bash
pkg update && pkg upgrade -y
pkg install git -y
git clone https://github.com/GlomGing85/FlexCLI.git
cd FlexCLI
```

### 2. Запуск інсталятора
```bash
bash install-termux.sh
```

### 3. Додавання NVIDIA API ключа
```bash
nano ~/.flexcli/.env
```

Встав:
```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Запуск FlexCLI
```bash
flexcli
```

## Оновлення
Якщо FlexCLI встановлено з GitHub:

```bash
cd ~/FlexCLI
bash update-termux.sh
```

## Конфігурація
Основний конфіг:

```bash
~/.flexcli/config.json
```

Приклад:

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
  "system_prompt": "Ти — FlexCLI..."
}
```

### Де зберігати API ключ
FlexCLI може читати `.env` з:
- `~/.flexcli/.env`
- `.env` у корені репозиторію
- `.env` у поточній папці запуску

Рекомендовано для Termux:

```bash
~/.flexcli/.env
```

## Модель пам'яті
Зараз FlexCLI використовує два простих рівні пам'яті:

### Коротка пам'ять
Остання історія діалогу в SQLite.

### Довга пам'ять
Окремо збережені корисні вподобання та нотатки.

Що корисно зберігати:
- улюблену мову програмування
- бажаний стиль відповідей
- назви проєктів
- важливі шляхи
- довготривалі задачі

## Генерація скілів
Інструмент `create_skill` зараз створює Python-заготовку в:

```bash
~/.flexcli/generated_skills/
```

Так зроблено спеціально.
Згенеровані скіли створюються безпечно і **не виконуються автоматично за замовчуванням**.

## Roadmap

### Alpha / MVP
- чат
- файлові інструменти
- пам'ять
- web search
- конфіг
- заготовки для скілів

### Наступні кроки
- streaming output
- `/mode chat|code|research`
- append/delete інструменти з підтвердженням
- безпечніше виконання коду
- автозавантаження generated skills
- кращий пошук і підсумки
- вибір мови CLI

## Внески
Дивись [CONTRIBUTING.md](CONTRIBUTING.md).

## Ліцензія
MIT — дивись [LICENSE](LICENSE).
