from flask import request, jsonify, abort
from app import app
from app.utils.file_handler import load_data, save_data

RECORD_FILE = 'records.json'
records = load_data(RECORD_FILE)


@app.route('/record', methods=['POST'])
def create_record():
    new_record = {
        'id': len(records) + 1,
        'user_id': request.json.get('user_id'),
        'category_id': request.json.get('category_id'),
        'date': request.json.get('date'),
        'amount': request.json.get('amount')
    }
    records.append(new_record)
    save_data(RECORD_FILE, records)
    return jsonify(new_record), 201

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = next((r for r in records if r['id'] == record_id), None)
    if not record:
        abort(404)
    return jsonify(record)


@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    filtered_records = [r for r in records if
                        (not user_id or r['user_id'] == int(user_id)) and
                        (not category_id or r['category_id'] == int(category_id))]

    if not filtered_records:
        abort(404)

    return jsonify(filtered_records)

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    global records
    records = [r for r in records if r['id'] != record_id]
    save_data(RECORD_FILE, records)  # Оновити збережені дані
    return '', 204
