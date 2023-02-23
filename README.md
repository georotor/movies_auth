# Проектная работа 6 спринта

Репозиторий с Auth API: https://github.com/georotor/Auth_sprint_1

Для запуска потребуется файл `.env.db` с переменными окружения для Postgresql:
```commandline
cp .env.db.example .env.db
```

Запуск сервиса осуществляется командой:
```commandline
docker-compose up -d --build
```

После первого запуска необходимо применить миграции для БД, для этого выполните команду:
```commandline
docker exec -it auth flask db upgrade
```

Для создания администратора воспользуйтесь командой:
```commandline
docker exec -it auth flask user --admin admin@example.com
```

### Документация
[Общая схема сервиса](https://github.com/georotor/Auth_sprint_1/blob/main/docs/Auth%20API.pdf).

Подробная документация доступна после запуска по адресу http://localhost/api/v1/



### Тестирование

Для запуска тестов потребуется файл `.env.tests` с переменными окружения:
```commandline
cp src/tests/functional/.env.tests.example src/tests/functional/.env.tests
```
Тесты запускаются командой:
```commandline
docker-compose -f src/tests/functional/docker-compose.tests.yml up --build
```
