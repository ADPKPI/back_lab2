from flask_smorest import Blueprint
from app.models import db, User
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

blp = Blueprint('auth', 'auth', url_prefix='/auth', description='Authentication routes')

@blp.route('/register', methods=['POST'])
def register():
    """Реєстрація нового користувача"""
    data = request.get_json()

    if User.query.filter_by(name=data["name"]).first():
        return {"message": "User already exists."}, 400

    hashed_password = pbkdf2_sha256.hash(data["password"])
    user = User(name=data["name"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered successfully."}, 201

@blp.route('/login', methods=['POST'])
def login():
    """Логін користувача"""
    data = request.get_json()
    user = User.query.filter_by(name=data["name"]).first()

    if user and pbkdf2_sha256.verify(data["password"], user.password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    return {"message": "Invalid credentials."}, 401

auth_bp = blp