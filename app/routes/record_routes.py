from flask_smorest import Blueprint
from flask.views import MethodView
from app.models import db, Record, Category
from app.models import RecordSchema
from flask import abort

# Обгортка для керування записами
blp = Blueprint('records', 'records', url_prefix='/record', description='Operations on records')

@blp.route('/')
class RecordList(MethodView):
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        """Отримати усі записи"""
        records = Record.query.all()
        return records

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        """Створити новий запис"""
        user_id = record_data['user_id']
        category_id = record_data['category_id']

        # Перевірка, що категорія належить користувачу або є глобальною
        category = Category.query.filter(
            (Category.id == category_id) &
            ((Category.user_id == user_id) | (Category.is_global == True))
        ).first()

        if not category:
            abort(403, description="You cannot use this category.")

        # Створення нового запису
        record = Record(**record_data)
        db.session.add(record)
        db.session.commit()
        return record

@blp.route('/<int:record_id>')
class RecordResource(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        """Отримати запис за ID"""
        record = Record.query.get_or_404(record_id)
        return record

    @blp.response(204)
    def delete(self, record_id):
        """Видалити запис"""
        record = Record.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return '', 204

# Регістрація Blueprint
record_bp = blp
