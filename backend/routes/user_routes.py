from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models.user import User
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ['name','email','password']):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        user = User(name=data['name'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User registered", "user":{"id":user.id,"name":user.name,"email":user.email}}),201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"Database error"}),500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(k in data for k in ['email','password']):
        return jsonify({"error":"Missing fields"}),400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": {"id": user.id, "name": user.name, "email": user.email}}),200
    return jsonify({"error":"Invalid credentials"}),401

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"User not found"}),404
    return jsonify({"id":user.id,"name":user.name,"email":user.email})
