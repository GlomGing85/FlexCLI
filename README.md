# FlexCLI

**FlexCLI** — CLI чат-агент для **Android + Termux**, заточений під:
- спілкування
- кодинг
- роботу з файлами та папками
- web search
- пам'ять
- створення нових скілів

> Поточний статус: **1.0.0-alpha.1**

Це **MVP / starter repo**, який уже підготовлений як GitHub-репозиторій і зручно ставиться / оновлюється на телефоні.

## Repo docs
- `README.md` — головна інструкція
- `CHANGELOG.md` — історія змін
- `CONTRIBUTING.md` — правила для внесків
- `RELEASE.md` — чекліст для релізів
- `LICENSE` — MIT

---

## 1. Що вже є в цьому репо

### Core
- CLI REPL
- агентний цикл через tool calling
- NVIDIA API client
- SQLite memory
- workspace sandbox
- JSON config

### Skills / Tools
- `list_files`
- `read_file`
- `write_file`
- `edit_file`
- `mkdir`
- `web_search`
- `save_memory`
- `search_memory`
- `create_skill`

### Команди в CLI
- `/help`
- `/config`
- `/mem`
- `/reset`
- `/set model <value>`
- `/set temp <value>`
- `/set search on|off`
- `/set genskills on|off`
- `/exit`

---

## 2. Структура репозиторію

```text
FlexCLI/
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ RELEASE.md
├─ install-termux.sh
├─ update-termux.sh
├─ run.sh
├─ pyproject.toml
├─ requirements.txt
├─ README.md
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

Після першого запуску буде створено:

```text
~/.flexcli/
├─ .env
├─ config.json
├─ memory.db
├─ generated_skills/
└─ workspace/
```

---

## 3. Публікація на GitHub

### Варіант A — якщо ти вже маєш цю папку локально

```bash
cd ~/FlexCLI
git init
git add .
git commit -m "Initial FlexCLI MVP"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/FlexCLI.git
git push -u origin main
```

### Варіант B — створити репо на GitHub спочатку
1. Зайди на GitHub.
2. Створи новий repo: `FlexCLI`.
3. Не додавай `README`, якщо ти вже маєш цей проєкт локально.
4. Скопіюй URL репозиторію.
5. Виконай команди з блоку вище.

---

## 4. Встановлення на Android через Termux

### Швидкий спосіб

```bash
pkg update && pkg upgrade -y
pkg install git -y
git clone https://github.com/<YOUR_GITHUB_USERNAME>/FlexCLI.git
cd FlexCLI
bash install-termux.sh
```

Після цього:

```bash
nano ~/.flexcli/.env
```

Встав свій ключ:

```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
```

Потім запуск:

```bash
flexcli
```

---

## 5. Оновлення з GitHub

Якщо ти поставив FlexCLI через `git clone`, оновлення робиться так:

```bash
cd ~/FlexCLI
bash update-termux.sh
```

Що робить `update-termux.sh`:
1. перевіряє, чи немає незакомічених змін
2. робить `git pull --ff-only`
3. перевстановлює Python-залежності
4. оновлює launcher-команду `flexcli`

> Якщо ти сам міняв код локально, спочатку зроби commit або stash.

---

## 6. Launcher-команда

Скрипт `install-termux.sh` автоматично створює глобальну команду:

```bash
flexcli
```

Вона запускає FlexCLI через `.venv`, тому тобі не потрібно щоразу вручну активувати virtualenv.

Якщо хочеш запустити прямо з папки проєкту:

```bash
./run.sh
```

---

## 7. Конфігурація

Файл:

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

### Де краще зберігати ключ
FlexCLI тепер читає `.env` з кількох місць:
- `~/.flexcli/.env`
- `.env` у корені репозиторію
- `.env` у поточній папці запуску

Рекомендований варіант для Termux:

```bash
~/.flexcli/.env
```

---

## 8. Як працює пам'ять

### Short-term memory
Останні повідомлення зберігаються в SQLite.

### Long-term memory
Окремі важливі факти зберігаються через `save_memory`.

Корисно зберігати:
- улюблену мову програмування
- стиль відповідей
- назви проєктів
- важливі шляхи
- довгі задачі

---

## 9. Як працює CreateSkill

`create_skill` зараз створює файл у:

```bash
~/.flexcli/generated_skills/
```

Це **безпечний starter-підхід**:
- агент генерує шаблон
- ти його переглядаєш
- ти сам вирішуєш, коли активувати логіку

Тобто агент не отримує автоматичне право виконувати довільний самогенерований код.

---

## 10. Roadmap

### V1
- чат
- файли
- пам'ять
- пошук
- налаштування
- create_skill

### V2
- streaming output
- `/mode chat|code|research`
- `append_file`
- `delete_file` з confirm
- `run_python`
- автозавантаження generated skills
- plugin loader

### V3
- voice mode
- sync між пристроями
- semantic memory
- локальні embeddings
- advanced tool registry

---

## 11. Типовий workflow для тебе

### Перший раз
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/FlexCLI.git
cd FlexCLI
bash install-termux.sh
nano ~/.flexcli/.env
flexcli
```

### Коли вийшло оновлення
```bash
cd ~/FlexCLI
bash update-termux.sh
```

### Коли хочеш змінити модель
У самому FlexCLI:

```text
/set model nvidia/llama-3.3-nemotron-super-49b-v1.5
```

---

## 12. Рекомендації по GitHub-репо

Зараз у репо вже є:
- `LICENSE` (MIT)
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `RELEASE.md`
- GitHub CI
- issue / PR templates

Я б радив далі:
- repo name: **FlexCLI**
- visibility: спочатку **private**, потім можна зробити public
- використовувати GitHub Releases
- додати `CHANGELOG`-нотатки до кожного релізу
- згодом додати окрему сторінку з прикладами скілів

Для alpha-версій зручно робити теги так:
- `v1.0.0-alpha.1`
- `v1.0.0-alpha.2`
- `v1.0.0-beta.1`

---

## 13. Якщо коротко

Щоб FlexCLI було зручно ставити й оновлювати, найкращий підхід такий:
- зберігати код у GitHub repo
- ставити через `git clone`
- інсталювати через `install-termux.sh`
- оновлювати через `update-termux.sh`
- ключ тримати в `~/.flexcli/.env`
- конфіг і пам'ять тримати в `~/.flexcli/`
