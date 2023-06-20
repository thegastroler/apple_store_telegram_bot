# Apple Store Telegram bot

<a href="https://t.me/GastrolerBot"><img src="https://img.shields.io/badge/Telegram-%20@GastrolerBot-blue"></a>

Pet-проект магазина по продаже техники apple в формате telegram-бота.

![screenshot](screenshot.png)

## Используемые технологии
* Python 3.8;
* aiogram 3.x (Telegram Bot framework);
* Docker and Docker Compose (контейнеризация);
* PostgreSQL (база данных);
* Redis (хранение данных для работы middleware);
* SQLAlchemy (работа с базой данных с помощью Python);
* Alembic (легкость миграций базы данных);
* Celery (периодичное выполнение задач для работы middleware)
* dependency-injector (удобное внедрение зависимостей)