# Bomber (мини-проэкт)

Небольшой фронтенд-проэкт с тремя файлами в корне:

- `index.html` — разметка
- `script.js` — логика клиента
- `style.css` — стили

Цель: заменить содержимое ветки `frontend` в репозитории https://github.com/Daniil2K6/Web_Minesweeper на файлы этого проекта.

Как использовать

1. Проверьте проект локально: откройте `index.html` в браузере.

2. Чтобы загрузить текущие файлы в удалённый репозиторий и заменить содержимое ветки `frontend`, используйте один из скриптов ниже или выполните команды вручную (см. раздел "Команды для пуша").

Безопасность

Для пуша на GitHub убедитесь, что у вас есть права на запись в репозиторий и настроена аутентификация (SSH ключи или Personal Access Token).

Команды для пуша (пример)

Пример с HTTPS и созданием отдельной (orphan) ветки `frontend`, которая заменит содержимое ветки на удалённом репозитории:

```bash
# В каталоге этого проекта
git init
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Daniil2K6/Web_Minesweeper.git
git fetch origin frontend || true
git checkout --orphan frontend
git rm -rf .
git add -A
git commit -m "Deploy frontend: replace branch content"
git push origin frontend --force
```

Если используете Personal Access Token (PAT) и хотите передать его в URL (менее безопасно), замените URL на:

`https://<TOKEN>@github.com/Daniil2K6/Web_Minesweeper.git`

Скрипты

- [push_frontend.sh](push_frontend.sh) — для Linux / macOS / Git Bash
- [push_frontend.bat](push_frontend.bat) — для Windows CMD

Примечание

Я не выполняю пуш в удалённый репозиторий от вашего имени. Ниже — готовые скрипты и команды; выполните их в своём окружении и подтвердите, если хотите, чтобы я помогал дальше.

---
Автор: автоматически сгенерировано
