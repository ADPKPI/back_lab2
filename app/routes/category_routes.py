from flask_smorest import Blueprint
from flask.views import MethodView
from app.models import db, Category, CategorySchema
from flask import request, abort
from flask_jwt_extended import jwt_required


# Обгортка для керування категоріями
blp = Blueprint('categories', 'categories', description='Operations on categories')

@blp.route('/')
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        """Отримати усі категорії (загальні та користувацькі)
        """
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            abort(400, description="`user_id` is required")

        categories = Category.query.filter(
            (Category.is_global == True) | (Category.user_id == user_id)
        ).all()
        return categories

    @blp.arguments(CategorySchema)
    @jwt_required()
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        """Створити нову категорію
        """
        user_id = category_data.get("user_id")
        is_global = category_data.get("is_global", False)

        # Перевірка: створення загальних категорій
        if is_global and not user_id:  # Загальні категорії створюються без зв'язку з користувачем
            category = Category(
                name=category_data["name"],
                is_global=True
            )
        else:
            if not user_id:
                abort(400, description="`user_id` is required for user-specific categories.")
            category = Category(
                name=category_data["name"],
                user_id=user_id,
                is_global=False
            )

        db.session.add(category)
        db.session.commit()
        return category

@blp.route('/<int:category_id>')
class CategoryResource(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        """Отримати категорію за ID
        """
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            abort(400, description="`user_id` is required")

        category = Category.query.filter(
            (Category.id == category_id) &
            ((Category.is_global == True) | (Category.user_id == user_id))
        ).first()

        if not category:
            abort(403, description="Access to this category is forbidden.")
        return category

    @blp.response(204)
    @jwt_required()
    def delete(self, category_id):
        """Видалити користувацьку категорію
        """
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            abort(400, description="`user_id` is required")

        category = Category.query.filter(
            (Category.id == category_id) &
            (Category.user_id == user_id)
        ).first()

        if not category:
            abort(403, description="You cannot delete this category.")
        if category.is_global:
            abort(403, description="Global categories cannot be deleted.")

        db.session.delete(category)
        db.session.commit()
        return '', 204

# Регістрація Blueprint
category_bp = blp
