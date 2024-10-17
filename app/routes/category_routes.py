from flask import request, jsonify, abort
from app import app
from app.utils.file_handler import load_data, save_data

CATEGORY_FILE = 'categories.json'
categories = load_data(CATEGORY_FILE)

@app.route('/category', methods=['POST'])
def create_category():
    new_category = {
        'id': len(categories) + 1,
        'name': request.json.get('name')
    }
    categories.append(new_category)
    save_data(CATEGORY_FILE, categories)
    return jsonify(new_category), 201

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    global categories
    categories = [c for c in categories if c['id'] != category_id]
    save_data(CATEGORY_FILE, categories)  # Оновити збережені дані
    return '', 204
