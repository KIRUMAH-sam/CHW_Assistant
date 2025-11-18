# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')  # Added email
    password = data.get('password')
    role = data.get('role', 'chw')

    if not username or not password or not email:
        return jsonify({"msg": "username, email, and password required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "username or email exists"}), 409

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "user created", "user_id": user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')  # login by email
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "bad email or password"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role}, expires_delta=timedelta(days=7))
    return jsonify({"access_token": access_token, "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}})
