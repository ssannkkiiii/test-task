# Lunch Service - Система управління обідами

Django REST API для управління ресторанами, меню та голосуванням за обіди.

## 🚀 Запуск проекту

### Варіант 1: Docker (Рекомендовано)

```bash
# Запустити проект
docker-compose up --build

# Запустити в фоновому режимі
docker-compose up -d --build
```

### Варіант 2: Локальний запуск

```bash
# Створити віртуальне середовище
python -m venv venv

# Активувати віртуальне середовище
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Встановити залежності
pip install -r requirements.txt

# Налаштувати базу даних (PostgreSQL)
# Створити базу даних 'lunch_service'

# Запустити міграції
python manage.py migrate

# Створити суперкористувача
python manage.py createsuperuser

# Запустити сервер
python manage.py runserver
```

## 🌐 Доступ до API

- **API Base URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📋 Тестування API в Postman

### 1. Налаштування Postman

1. Відкрийте Postman
2. Створіть нову колекцію "Lunch Service API"
3. Додайте змінну середовища:
   - `base_url`: `http://localhost:8000`

### 2. Аутентифікація

#### Реєстрація користувача
```
POST {{base_url}}/api/v1/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "date_of_birth": "1990-01-01",
    "password": "testpass123",
    "password_confirm": "testpass123"
}
```

#### Вхід в систему
```
POST {{base_url}}/api/v1/auth/login/
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "testpass123"
}
```

**Збережіть `access_token` з відповіді для подальших запитів!**

### 3. Профіль користувача

#### Отримати профіль
```
GET {{base_url}}/api/v1/auth/profile/
Authorization: Bearer {{access_token}}
```

#### Оновити профіль
```
PATCH {{base_url}}/api/v1/auth/profile/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "first_name": "Updated Name",
    "last_name": "Updated Lastname"
}
```

#### Змінити пароль
```
PATCH {{base_url}}/api/v1/auth/change-password/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "old_password": "testpass123",
    "new_password": "newpass123",
    "new_password_confirm": "newpass123"
}
```

### 4. Ресторани

#### Отримати список ресторанів
```
GET {{base_url}}/api/v1/restaurants/
Authorization: Bearer {{access_token}}
```

#### Отримати деталі ресторану
```
GET {{base_url}}/api/v1/restaurants/1/
Authorization: Bearer {{access_token}}
```

#### Створити ресторан (тільки адміністратори)
```
POST {{base_url}}/api/v1/restaurants/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "name": "Новий ресторан",
    "description": "Опис ресторану",
    "address": "Вулиця, 123",
    "phone_number": "+380123456789",
    "email": "restaurant@example.com",
    "website": "https://restaurant.com"
}
```

#### Оновити ресторан (тільки адміністратори)
```
PATCH {{base_url}}/api/v1/restaurants/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "name": "Оновлена назва ресторану"
}
```

#### Видалити ресторан (тільки адміністратори)
```
DELETE {{base_url}}/api/v1/restaurants/1/
Authorization: Bearer {{access_token}}
```

#### Пошук ресторанів
```
GET {{base_url}}/api/v1/restaurants/search/?q=назва
Authorization: Bearer {{access_token}}
```

### 5. Меню

#### Отримати список меню
```
GET {{base_url}}/api/v1/menus/
Authorization: Bearer {{access_token}}
```

#### Створити меню (тільки адміністратори)
```
POST {{base_url}}/api/v1/menus/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "restaurant": 1,
    "date": "2024-01-15",
    "items": [
        {
            "name": "Борщ",
            "description": "Традиційний український борщ",
            "price": 50.00
        },
        {
            "name": "Котлета по-київськи",
            "description": "Куряча котлета з маслом",
            "price": 80.00
        }
    ]
}
```

### 6. Голосування

#### Проголосувати за ресторан
```
POST {{base_url}}/api/v1/voting/vote/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "menu": 1
}
```

#### Отримати свій голос на сьогодні
```
GET {{base_url}}/api/v1/voting/today-vote/
Authorization: Bearer {{access_token}}
```

#### Скасувати голос
```
DELETE {{base_url}}/api/v1/voting/cancel-vote/
Authorization: Bearer {{access_token}}
```

#### Отримати результати голосування на сьогодні
```
GET {{base_url}}/api/v1/voting/today-results/
Authorization: Bearer {{access_token}}
```

#### Отримати історію голосування
```
GET {{base_url}}/api/v1/voting/history/
Authorization: Bearer {{access_token}}
```

### 7. Співробітники

#### Отримати список співробітників
```
GET {{base_url}}/api/v1/employees/
Authorization: Bearer {{access_token}}
```

#### Отримати деталі співробітника
```
GET {{base_url}}/api/v1/employees/1/
Authorization: Bearer {{access_token}}
```

## 🔧 Корисні команди

### Docker команди
```bash
# Переглянути логи
docker-compose logs -f

# Зупинити сервіси
docker-compose down

# Перезапустити сервіси
docker-compose restart

# Видалити все (контейнери, образи, томи)
docker-compose down -v
docker system prune -f
```

### Django команди
```bash
# Запустити тести
python manage.py test
# або
pytest

# Створити міграції
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Створити суперкористувача
python manage.py createsuperuser

# Зібрати статичні файли
python manage.py collectstatic
```

## 📝 Примітки

- Всі API ендпоінти потребують аутентифікації (крім реєстрації та входу)
- Використовуйте JWT токени для авторизації
- Тільки адміністратори можуть створювати/редагувати/видаляти ресторани та меню
- Голосування можна проводити тільки один раз на день
- API підтримує пагінацію (20 елементів на сторінку)

## 🐛 Налагодження

Якщо виникають проблеми:

1. Перевірте, чи запущені контейнери: `docker-compose ps`
2. Перегляньте логи: `docker-compose logs`
3. Перевірте підключення до бази даних
4. Переконайтеся, що всі міграції застосовані
