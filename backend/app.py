# backend/app.py
from flask import Flask, jsonify
from config import Config
from extensions import init_extensions, db
from routes.auth_routes import auth_bp
from routes.case_routes import case_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)

    # register routes
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(case_bp, url_prefix='/api/v1/cases')

    @app.route('/')
    def index():
        return jsonify({"message": "CHW Decision Assistant API running"})

    return app
