# Лабораторна робота №3

**Варіант завдання: 23 % 3 = 2**

### Завдання:

Для користувацьких категорій витрат - повинні бути загальні категорії витрат, які видно всім користувачам, та користувацькі, які можуть вказати тільки користувачі, які їх визначили.

---

### Public URL: http://5.11.83.35:10000

### Documentation: http://5.11.83.35:10000/docs

## Зміни, внесені у проект:

### 1. Створення бази даних у Docker-контейнері
- Використано PostgreSQL для зберігання даних.
- Створено `docker-compose.yml` для налаштування контейнерів з базою даних та застосунком.

### 2. Модифікація моделі даних
#### Додано нові таблиці:
- **User**:
  - `id` (integer, primary key)
  - `name` (string, not null)
- **Category**:
  - `id` (integer, primary key)
  - `name` (string, not null)
  - `is_global` (boolean, default=false)
  - `user_id` (foreign key на User, nullable)
- **Record**:
  - `id` (integer, primary key)
  - `user_id` (foreign key на User, not null)
  - `category_id` (foreign key на Category, not null)
  - `date` (date, not null)
  - `amount` (float, not null)

### 3. Реалізація через ORM (SQLAlchemy)
- Використано SQLAlchemy для опису моделей.
- Міграції виконані за допомогою Flask-Migrate.

### 4. Додано ендпоінти:
#### **User**:
- `POST /user/` - створити користувача.
- `GET /user/` - отримати список усіх користувачів.
- `GET /user/<user_id>` - отримати конкретного користувача за ID.
- `DELETE /user/<user_id>` - видалити користувача.

#### **Category**:
- `GET /category/` - отримати всі категорії (загальні та користувацькі).
- `POST /category/` - створити нову категорію.
- `GET /category/<category_id>` - отримати категорію за ID.
- `DELETE /category/<category_id>` - видалити користувацьку категорію.

#### **Record**:
- `GET /record/` - отримати всі записи.
- `POST /record/` - створити новий запис.
- `GET /record/<record_id>` - отримати запис за ID.
- `DELETE /record/<record_id>` - видалити запис.

### 5. Логіка для категорій:
- Загальні категорії (`is_global = True`) доступні для всіх користувачів.
- Користувацькі категорії (`is_global = False`) доступні лише користувачам, які їх створили.

---