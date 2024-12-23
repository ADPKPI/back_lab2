from flask_smorest import Blueprint
from app.models import db, User
from app.models import UserSchema

# Обєкт для обобліку користувачів
blp = Blueprint('users', 'users', url_prefix='/user', description='Operations on users')

# Маршрут створення користувача
@blp.route('/', methods=['POST'])
@blp.arguments(UserSchema)
@blp.response(201, UserSchema)
def create_user(user_data):
    """
    Створення нового користувача
    """
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    return user

# Маршрут отримання усіх користувачів
@blp.route('/', methods=['GET'])
@blp.response(200, UserSchema(many=True))
def get_users():
    """
    Отримати усіх користувачів
    """
    users = User.query.all()
    return users

# Маршрут отримання користувача за ID
@blp.route('/<int:user_id>', methods=['GET'])
@blp.response(200, UserSchema)
def get_user(user_id):
    """
    Отримати користувача за його ID
    """
    user = User.query.get_or_404(user_id)
    return user

# Маршрут видалення користувача за ID
@blp.route('/<int:user_id>', methods=['DELETE'])
@blp.response(204)
def delete_user(user_id):
    """
    Видалити користувача за його ID
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Реєстрація обєкта Blueprint
user_bp = blp
