# Web_Minesweeper — Backend (Django)

Этот README описывает, как запустить и отладить серверную часть проекта.

Требования
- Python 3.8+
- Установленные зависимости (см. requirements.txt, если есть)

Запуск локально
```bash
python -m pip install -r requirements.txt
python saper_backend/manage.py makemigrations
python saper_backend/manage.py migrate
python saper_backend/manage.py runserver
```

Основные пути API
- `GET /api/leaderboard` — получить таблицу лидеров
- `POST /api/save-score` — сохранить результат (принимает `time`, `username`, `created_at`)
- `POST /api/register` — регистрация (SimpleUser)
- `POST /api/login` — вход

База данных
- Файл базы — `saper_backend/db.sqlite3`
- Утилита для просмотра: `db_viewer.py`

Миграции
- Миграции находятся в `saper_backend/api/migrations/`

Полезные команды
-- Посмотреть таблицу пользователей:
```bash
python -c "import saper_backend.db_viewer as dv; dv.print_table('api_simpleuser')"
```
-- Посмотреть лидерборд:
```bash
python -c "import saper_backend.db_viewer as dv; dv.print_table('api_leaderboard')"
```

Примечание
- Сервер использует простую модель `SimpleUser` и не завязан на Django auth для всех эндпоинтов; будьте внимательны при тестировании сессий и CSRF.
