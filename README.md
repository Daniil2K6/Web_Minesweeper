# Web Minesweeper — Быстрый старт

Ниже — проверенные однострочные команды для PowerShell и bash, которые можно копировать и вставлять.

PowerShell (Windows):

- Клонировать и перейти в папку: `git clone https://github.com/Daniil2K6/Web_Minesweeper.git; cd Web_Minesweeper`
- Создать и активировать venv: `python -m venv .venv; .\.venv\Scripts\Activate`
- Установить зависимости: `python -m pip install -r requirements.txt || python -m pip install django djangorestframework django-cors-headers`
- Применить миграции: `python saper_backend/manage.py migrate`
- Запустить сервер: `python saper_backend/manage.py runserver`
- Открыть фронтенд (локально): `Start-Process Bomber\index.html`
- Просмотреть все таблицы БД: `python saper_backend/db_viewer.py`
- Просмотреть таблицу `api_simpleuser`: `python -c "import saper_backend.db_viewer as dv; dv.print_table('api_simpleuser')"`
- Просмотреть таблицу `api_leaderboard`: `python -c "import saper_backend.db_viewer as dv; dv.print_table('api_leaderboard')"`

bash (Linux / macOS):

- Клонировать и перейти: `git clone https://github.com/Daniil2K6/Web_Minesweeper.git; cd Web_Minesweeper`
- Создать и активировать venv: `python3 -m venv .venv; source .venv/bin/activate`
- Установить зависимости: `python3 -m pip install -r requirements.txt || python3 -m pip install django djangorestframework django-cors-headers`
- Применить миграции: `python3 saper_backend/manage.py migrate`
- Запустить сервер: `python3 saper_backend/manage.py runserver`
- Открыть фронтенд (локально): `xdg-open Bomber/index.html || open Bomber/index.html`
- Просмотреть таблицы БД: `python3 -c "import saper_backend.db_viewer as dv; dv.print_all_tables()"`

Примечание: все команды рассчитаны на то, что вы выполняете их из корня репозитория `Web_Minesweeper`.
Если нужно, могу добавить `requirements.txt` и автоматизированные скрипты.
