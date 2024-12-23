import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from app.routes.user_routes import user_bp
from app.routes.category_routes import category_bp
from app.routes.record_routes import record_bp
from app.models import db
from flask_migrate import Migrate

def create_app():
    """
    Створення та налаштування застосунку Flask.
    """
    app = Flask(__name__)

    # Конфігурація бази даних
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab_user:lab_password@db:5432/lab_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Налаштування OpenAPI
    app.config.from_mapping({
        'API_TITLE': 'My API',  # Назва API
        'API_VERSION': 'v1',  # Версія API
        'OPENAPI_VERSION': '3.0.3',  # Версія OpenAPI
        'OPENAPI_URL_PREFIX': '/docs',  # Префікс для документації
        'OPENAPI_SWAGGER_UI_PATH': '/',  # Шлях до Swagger UI
        'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'  # URL Swagger UI
    })

    # Ініціалізація бази даних
    db.init_app(app)

    # Ініціалізація Flask-Migrate для управління міграціями
    migrate = Migrate(app, db)

    # Ініціалізація API
    api = Api(app)

    # Створення таблиць (якщо вони ще не створені)
    with app.app_context():
        db.create_all()

    # Реєстрація маршрутів
    api.register_blueprint(user_bp, url_prefix='/user')  # Роутинг для користувачів
    api.register_blueprint(category_bp, url_prefix='/category')  # Роутинг для категорій
    api.register_blueprint(record_bp, url_prefix='/record')  # Роутинг для записів

    return app
