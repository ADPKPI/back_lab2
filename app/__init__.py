import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from app.routes.user_routes import user_bp
from app.routes.category_routes import category_bp
from app.routes.record_routes import record_bp
from app.routes.auth_routes import auth_bp
from app.models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask import jsonify


def create_app():
    """
    Створення та налаштування застосунку Flask.
    """
    app = Flask(__name__)
    jwt = JWTManager(app)

    # Конфігурація бази даних
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab_user:lab_password@db:5432/lab_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Налаштування OpenAPI
    app.config.from_mapping({
        'API_TITLE': 'Lab4',  # Назва API
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
    api.register_blueprint(auth_bp, url_prefix='/auth')  # Роутинг для записів

    # Обробники помилок JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {"description": "Request does not contain an access token.", "error": "authorization_required"}), 401

    return app
