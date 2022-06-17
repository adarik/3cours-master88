## Привет!

### Это проект курсового проекта №3 SkyPro. Сложная версия (MVC архитектура)

В данном курсовом проекте было создано Flask приложение с построением MVC архитектуры, 
использованием flask-restx и базы данных SQLite, контролем доступа пользователей, хешированием паролей, использованием 
JSON Web Token (JWT), написание unit-тестов при помощибиблиотек pytest, unittest.

В проэкте собран **Docker** контейнер, как с помощью обычного DockerFile, так и с использованием docker-compose. Реализована сборка контейнера и деплой на хостинг в парадигме **CI\CD** с помощью **GitHub Actions**. Использованы secrets для скрытия данных. Проект выложен на Docker Hub (https://hub.docker.com/repository/docker/dwayneward/hw_26).
Также совершен деплой бэк-энда вэб сайта на хостинг (vleontev.ga/docs - откроет вам страницу документации Flask)


**Отработаны навыки** работы с SQLAlchemy, работы с Class-Based-View(CBV) фреймворка flask-restx, написание и
использование сериализаторов фреймворка marshmallow, построения MVC архитектуры Flask приложения, работы с JWT, 
хешированием паролей. Также были написаны тесты для некоторых процессов работы прилоения. Изучен Docker, docker-compose. Собран контейнер 

Если вы хотите запустить приложение на локальной машине, необходимо клонировать репозиторий и установить flask, flask-sqlalchemy, sqlalchemy, marshmallow,
flask_restx и кучу всякого. Для этого используйте файл requirements.txt (pip/pip3 install -r requirements.txt)



### Запуск проекта

#### Bash (Linux/MACOS)
```shell
export FLASK_APP=run.py
export FLASK_ENV='development'
flask run
```

#### CMD (Windows)
```shell
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

#### PowerShell (Windows)
```shell
$env:FLASK_APP = "run"
$env:FLASK_ENV = "development"
flask run
```

### Запуск тестов
```shell
pytest .
```

## Приятного использования! 
