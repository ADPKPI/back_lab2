from flask import request, jsonify, abort
from app import app
from app.utils.file_handler import load_data, save_data

USER_FILE = 'users.json'
users = load_data(USER_FILE)

@app.route('/user', methods=['POST'])
def create_user():
    new_user = {
        'id': len(users) + 1,
        'name': request.json.get('name')
    }
    users.append(new_user)
    save_data(USER_FILE, users)
    return jsonify(new_user), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        abort(404)
    return jsonify(user)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    save_data(USER_FILE, users)
    return '', 204
