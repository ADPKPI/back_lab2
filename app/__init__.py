from flask import Flask

app = Flask(__name__)

from app.routes import user_routes, category_routes, record_routes