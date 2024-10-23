# Study

Приложение Study на Django Rest Framework онлайн обучений.

## Стек технологий

- **Python**
- **Django**
- **Django Rest Framework (DRF)**
- **PostgreSQL**
- **Redis**
- **Celery**
- **Docker**
- **Docker-compose**

## Инструкция по запуску проекта

### 1. Клонируйте репозиторий

Сначала клонируйте репозиторий на ваш локальный компьютер:

```bash
git clone https://github.com/egororlov3/Kursovaya7.git
```

### 2. Docker Compose

После клонирования репозитория введите в терминале команды:
```bash
docker-compose build

docker-compose up 
```

### 3. Установка без Docker Compose 

- После клонирования введите следующие команды в терминале:
```bash
python -m venv venv

venv/scripts/activate

pip install -r requirements.txt
```

- Применение миграций для связи с БД
```bash
python manage.py migrate
```

- Созадйте супер пользователя
```bash
python manage.py createsuperuser 
```

- Запустите сервер
```bash
python manage.py runserver 
```
# END

## Теперь в ваших руках целый проект по онлайн обучению) 
