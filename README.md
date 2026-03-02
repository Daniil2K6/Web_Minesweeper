# Web Minesweeper — Быстрый старт

Ниже — аккуратно оформленное руководство с рабочими командами. Копируйте и вставляйте команды прямо в терминал (без Markdown-обрамления). Если вы видите в README строки в обратных кавычках (`` ` ``) — это для форматирования, в терминале их не вводите.

## PowerShell (Windows)

- Клонировать и перейти в папку:

```powershell
git clone https://github.com/Daniil2K6/Web_Minesweeper.git; cd Web_Minesweeper
```

- Создать и активировать виртуальное окружение:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate
```

- Установить зависимости (если есть `requirements.txt`, иначе установит минимальные пакеты):

```powershell
python -m pip install -r requirements.txt || python -m pip install django djangorestframework django-cors-headers
```

- Применить миграции:

```powershell
python saper_backend/manage.py migrate
```

- Запустить сервер разработки (оставит вывод в терминале):

```powershell
python saper_backend/manage.py runserver
```

- Открыть фронтенд (локально) в браузере:

```powershell
Start-Process Bomber\index.html
```

- Просмотреть все таблицы БД (скрипт расположен в `saper_backend/db_viewer.py`):

```powershell
python saper_backend/db_viewer.py
```

- Просмотреть таблицу `api_simpleuser`:

```powershell
python -c "import saper_backend.db_viewer as dv; dv.print_table('api_simpleuser')"
```

- Просмотреть таблицу `api_leaderboard`:

```powershell
python -c "import saper_backend.db_viewer as dv; dv.print_table('api_leaderboard')"
```

## Bash (Linux / macOS)

- Клонировать и перейти в папку:

```bash
git clone https://github.com/Daniil2K6/Web_Minesweeper.git; cd Web_Minesweeper
```

- Создать и активировать виртуальное окружение:

```bash
python3 -m venv .venv; source .venv/bin/activate
```

- Установить зависимости:

```bash
python3 -m pip install -r requirements.txt || python3 -m pip install django djangorestframework django-cors-headers
```

- Применить миграции:

```bash
python3 saper_backend/manage.py migrate
```

- Запустить сервер разработки:

```bash
python3 saper_backend/manage.py runserver
```

- Открыть фронтенд (локально):

```bash
xdg-open Bomber/index.html || open Bomber/index.html
```

- Просмотреть таблицы БД:

```bash
python3 -c "import saper_backend.db_viewer as dv; dv.print_all_tables()"
```

## Примечания и советы

- Выполняйте команды из корня репозитория `Web_Minesweeper`.
- Если вы видите в README команды, окружённые обратными кавычками (`` ` ``), не вводите эти обратные кавычки в терминале — они только для форматирования в Markdown.
- Если виртуальное окружение активно и вы хотите выйти, выполните в терминале:

```powershell
deactivate
```

или в bash:

```bash
deactivate
```

Если `deactivate` не найдена, значит окружение в этой сессии не активно.

Если хотите, я добавлю `requirements.txt` с необходимыми версиями и экспортирую текущие таблицы БД в `saper_backend/exports/`.

