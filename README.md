![YaMDB workflow](https://github.com/KaterinaSolovyeva/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Описание.

Проект «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Адрес, на котором всё это можно видеть в сборе:
- Сайт «Продуктовый помощник»:
http://www.yatubeproject.tk
или http://www.yatubeproject.tk/recipes/
- Администрирование
http://www.yatubeproject.tk/admin/
- API
http://www.yatubeproject.tk/api/

ТЕСТОВЫЙ ПОЛЬЗОВАТЕЛЬ:
   - "email": "vpupkin@yandex.ru",
   - "username": "vasya.pupkin",
   - "first_name": "Вася",
   - "last_name": "Пупкин",
   - "password": "вап-вап-dfg"

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/KaterinaSolovyeva/foodgram-project-react

```
```
cd foodgram-project-react
```
Создайте файл .env командой touch .env. Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
```
Запустите docker-compose командой sudo docker-compose up -d
```
Создайте миграции: 
```
docker-compose exec backend python manage.py migrate --noinput
```
Соберите статику проекта командой:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Создайте суперпользователя Django:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Загрузите тестовые данные в базу данных командой: 
```
sudo docker -compose exec backend python manage.py loaddata dump.json
```
