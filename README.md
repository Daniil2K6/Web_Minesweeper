### Удаление пользователя по id
Для удаления пользователя (только для администратора) используйте:
```bash
python saper_backend/manage.py shell -c "from api.models import SimpleUser; SimpleUser.objects.filter(id=USER_ID).delete()"
```
Замените USER_ID на нужный id пользователя.
# browser-based-minesweeper
## Быстрый старт

### Запуск базы данных (Django backend)
```bash
python saper_backend/manage.py runserver
```

### Запуск веб-страницы (frontend)
Откройте файл `templates/index.html` в браузере или настройте сервер для статики.

### Вывод всех таблиц из базы данных
```bash
python db_viewer.py
```

### Вывод таблицы пользователей (SimpleUser)
```bash
python -c "import db_viewer; db_viewer.print_table('api_simpleuser')"
```

### Вывод таблицы результатов (Leaderboard)
```bash
python -c "import db_viewer; db_viewer.print_table('api_leaderboard')"
```

### Описание таблицы пользователей
Таблица `api_simpleuser` содержит:
- username — имя пользователя
- password — пароль
- best_time — лучшее время
- data_top_game — дата лучшей игры (добавить в модель)

### Вывод конкретной таблицы
```bash
python -c "import db_viewer; db_viewer.print_table('имя_таблицы')"
```