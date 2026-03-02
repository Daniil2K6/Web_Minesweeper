# Web Minesweeper — Быстрый старт

Структура репозитория после простого клона должна содержать в корне только:
- `Bomber/` — фронтенд (статические файлы)
- `saper_backend/` — Django backend
- `README.md` — инструкции ниже

Шаги для запуска (Windows):

1) Клонировать репозиторий и перейти в папку:

```powershell
git clone https://github.com/Daniil2K6/Web_Minesweeper.git; cd Web_Minesweeper
```

2) (Рекомендуется) Создать виртуальное окружение и активировать:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate
```

3) Установить зависимости (если у вас нет `requirements.txt`, установите вручную):

```powershell
python -m pip install -r requirements.txt || python -m pip install django djangorestframework django-cors-headers
```

4) Применить миграции базы данных:

```powershell
python saper_backend/manage.py migrate
```

5) Запустить сервер разработки:

```powershell
python saper_backend/manage.py runserver
```

6) Открыть в браузере http://127.0.0.1:8000/ — должна загрузиться игра.

Проверки и вспомогательные команды:

- Просмотреть все таблицы базы данных (скрипт находится в `saper_backend/db_viewer.py`):

```powershell
python saper_backend/db_viewer.py
```

- Вывести конкретную таблицу (пример `api_leaderboard`):

```powershell
python -c "import saper_backend.db_viewer as dv; dv.print_table('api_leaderboard')"
```

- Запустить фронтенд локально, открыв статический файл (альтернатива):

```powershell
Start-Process Bomber\index.html
```

Linux / macOS примеры отличаются только командами активации venv и открытия файла:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt || python3 -m pip install django djangorestframework django-cors-headers
python3 saper_backend/manage.py migrate
python3 saper_backend/manage.py runserver
# открыть http://127.0.0.1:8000/
```

Если нужно посмотреть статус репозитория или очистить лишние локальные файлы:

```bash
git status --porcelain
git clean -fdx   # Удалит неотслеживаемые файлы (локальный .venv и т.д.) — использовать с осторожностью
```

Если понадобятся дополнительные инструкции по развёртыванию или упаковке в Docker — скажите, добавлю.
