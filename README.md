# Проектная работа 6 и 7 спринта

Репозитории:
- Auth API: https://github.com/georotor/Auth_sprint_1
- Async API: https://github.com/georotor/Async_API_sprint_1


Для запуска потребуется файл `.env.db` с переменными окружения для Postgresql:
```commandline
cp .env.db.example .env.db
```

и `.env.oauth` с данными для авторизации через сторонние сервисы:
```commandline
cp .env.oauth.example .env.oauth
```

Запуск Auth сервиса осуществляется командой:
```commandline
docker-compose up -d --build
```

После первого запуска необходимо применить миграции БД, для этого выполните команду:
```commandline
docker exec -it auth flask db upgrade
```

Для создания администратора воспользуйтесь командой:
```commandline
docker exec -it auth flask user --admin admin@example.com
```


## Трассировка
Так же после запуска доступен Jaeger: http://localhost:16686


## Документация
Подробная документация доступна после запуска по адресу http://localhost/api/v1/


## Тестирование

Для запуска тестов потребуется файл `.env.tests` с переменными окружения:
```commandline
cp src/tests/functional/.env.tests.example src/tests/functional/.env.tests
```
Тесты запускаются командой:
```commandline
docker-compose -f src/tests/functional/docker-compose.tests.yml up --build
```
