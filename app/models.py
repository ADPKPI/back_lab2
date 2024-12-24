from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

# Модель користувача
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор користувача
    name = db.Column(db.String(128), nullable=False)  # Ім'я користувача
    password = db.Column(db.String(128), nullable=False)  # Пароль користувача


# Модель категорії
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор категорії
    name = db.Column(db.String(128), nullable=False)  # Назва категорії
    is_global = db.Column(db.Boolean, default=False)  # Чи категорія глобальна
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Прив'язка до користувача, якщо не глобальна

# Модель запису
class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор запису
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Прив'язка до користувача
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Прив'язка до категорії
    date = db.Column(db.Date, nullable=False)  # Дата запису
    amount = db.Column(db.Float, nullable=False)  # Сума запису

# Схема для валідації користувачів
class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # Унікальний ідентифікатор (тільки для читання)
    name = fields.Str(required=True)  # Ім'я користувача (обов'язкове)
    password = fields.Str(load_only=True, required=True)

# Схема для валідації категорій
class CategorySchema(Schema):
    id = fields.Int(dump_only=True)  # Унікальний ідентифікатор (тільки для читання)
    name = fields.Str(required=True)  # Назва категорії (обов'язкова)
    is_global = fields.Bool(required=True)  # Чи категорія глобальна
    user_id = fields.Int()  # Ідентифікатор користувача

# Схема для валідації записів
class RecordSchema(Schema):
    id = fields.Int(dump_only=True)  # Унікальний ідентифікатор (тільки для читання)
    user_id = fields.Int(required=True)  # Ідентифікатор користувача (обов'язкове поле)
    category_id = fields.Int(required=True)  # Ідентифікатор категорії (обов'язкове поле)
    date = fields.Date(required=True)  # Дата запису (обов'язкове поле)
    amount = fields.Float(required=True)  # Сума запису (обов'язкове поле)
