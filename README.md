Backend REST API для платформы онлайн-курсов на Django REST Framework.

## 🚀 Технологии

- Python 3.13
- Django 5.1.4
- Django REST Framework 3.15.2
- PostgreSQL
- Basic Authentication
- Swagger/OpenAPI документация

## 📋 Возможности

- ✅ Регистрация и аутентификация пользователей (username/email/phone)
- ✅ Управление курсами, модулями и уроками
- ✅ Покупка курсов с различными методами оплаты
- ✅ Отслеживание прогресса обучения
- ✅ Система отзывов и рейтингов
- ✅ Автоматическая генерация сертификатов
- ✅ Техподдержка (messaging система)
- ✅ FAQ и отзывы (testimonials)
- ✅ Админ-панель для управления контентом

## 🔧 Локальная установка

### Требования

- Python 3.13+
- PostgreSQL 15+

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Шаг 2: Создание виртуального окружения
```bash
python -m venv venv

# Активация (macOS/Linux)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate
```

### Шаг 3: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка PostgreSQL
```sql
-- Войдите в PostgreSQL
psql postgres

-- Создайте базу данных
CREATE DATABASE courses_db;

-- Создайте пользователя
CREATE USER courses_user WITH PASSWORD 'your_password';

-- Дайте права
GRANT ALL PRIVILEGES ON DATABASE courses_db TO courses_user;

-- Выйдите
\q
```

### Шаг 5: Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
PGDATABASE=courses_db
PGUSER=courses_user
PGPASSWORD=your_password
PGHOST=localhost
PGPORT=5432
```

### Шаг 6: Применение миграций
```bash
python manage.py migrate
```

### Шаг 7: Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Шаг 8: Загрузка тестовых данных (опционально)
```bash
python manage.py test_data
```

Это создаст:
- 2 тестовых студента (student1, student2 / password: student123)
- 3 спикера
- 3 курса с модулями и уроками
- FAQ и testimonials

### Шаг 9: Запуск сервера
```bash
python manage.py runserver
```

Сервер будет доступен на `http://127.0.0.1:8000`

## 📚 API Документация

### Swagger UI (интерактивная документация)
```
http://127.0.0.1:8000/swagger/
```

### ReDoc (альтернативная документация)
```
http://127.0.0.1:8000/redoc/
```

### Админ-панель
```
http://127.0.0.1:8000/admin/
```

## 🔐 Аутентификация

API использует **HTTP Basic Authentication**.

### Пример использования (JavaScript):
```javascript
// С Axios
axios.get('http://127.0.0.1:8000/api/courses/', {
  auth: {
    username: 'student1',
    password: 'student123'
  }
});

// С Fetch
const credentials = btoa('student1:student123');
fetch('http://127.0.0.1:8000/api/courses/', {
  headers: {
    'Authorization': `Basic ${credentials}`
  }
});
```

### Пример (Python):
```python
import requests

response = requests.get(
    'http://127.0.0.1:8000/api/courses/',
    auth=('student1', 'student123')
)
```

## 🌐 Основные эндпоинты

### Аутентификация
```
POST   /api/auth/register/          - Регистрация
POST   /api/auth/login/              - Логин (username/email/phone)
POST   /api/auth/logout/             - Выход
GET    /api/auth/check/              - Проверка авторизации
GET    /api/auth/profile/            - Профиль пользователя
PUT    /api/auth/profile/            - Обновление профиля
POST   /api/auth/change-password/    - Смена пароля
```

### Курсы
```
GET    /api/courses/                 - Список курсов
GET    /api/courses/{slug}/          - Детали курса
GET    /api/courses/{slug}/free/     - Бесплатный урок
```

### Мои курсы (требуется авторизация)
```
GET    /api/my-courses/              - Купленные курсы
GET    /api/my-courses/{id}/progress/ - Прогресс по курсу
```

### Покупки
```
POST   /api/purchases/create/        - Создать покупку
GET    /api/purchases/               - История покупок
```

### Уроки
```
GET    /api/lessons/{id}/            - Детали урока
POST   /api/lessons/{id}/progress/   - Обновить прогресс
```

### Отзывы
```
GET    /api/reviews/                 - Список отзывов
POST   /api/reviews/create/          - Создать отзыв
GET    /api/my-reviews/              - Мои отзывы
```

### Сертификаты
```
GET    /api/certificates/            - Мои сертификаты
POST   /api/certificates/generate/{course_id}/ - Сгенерировать сертификат
```

### Публичные
```
GET    /api/faq/                     - FAQ
GET    /api/testimonials/            - Отзывы клиентов
GET    /api/settings/                - Настройки сайта
GET    /api/speakers/                - Список спикеров
```

## 🧪 Тестовые данные

После запуска `python manage.py test_data` доступны:

### Тестовые пользователи:

- **student1** / student123
- **student2** / student123
- **admin** / admin123 (суперпользователь)

### Тестовые курсы:

1. Таргетированная реклама для начинающих (4999 KGS)
2. SMM и контент-маркетинг (5999 KGS)
3. Мобильная фотография (3999 KGS)

## 🚀 Деплой

### Railway.app

1. Подключите GitHub репозиторий
2. Добавьте PostgreSQL database
3. Настройте переменные окружения:
```
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=.railway.app,.up.railway.app
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=secure_password
```
4. Deploy автоматически запустится

### Heroku / DigitalOcean

См. документацию соответствующих платформ.

## 📁 Структура проекта
```
.
├── config/                 # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── courses/                # Основное приложение
│   ├── management/
│   │   └── commands/
│   │       └── test_data.py  # Команда для тестовых данных
│   ├── models.py           # Модели БД
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # URL маршруты
│   └── admin.py            # Админ-панель
├── manage.py
├── requirements.txt
├── Procfile                # Для Railway/Heroku
├── runtime.txt             # Версия Python
├── setup_admin.py          # Скрипт создания админа
└── README.md
```

## 🛠️ Разработка

### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск тестов
```bash
python manage.py test
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Сбор статических файлов
```bash
python manage.py collectstatic
```

## 🔒 Безопасность

- ✅ CSRF защита отключена для API (используется Basic Auth)
- ✅ HTTPS обязателен в продакшене
- ✅ Секретные ключи в переменных окружения
- ✅ Валидация паролей
- ✅ Rate limiting (можно настроить в DRF)

## 📝 Лицензия

[]

## 👥 Авторы

[Okurmen IT Studio]

## 📧 Контакты

- Email: support@skillsup.kg
- Website: https://skillsup.kg


