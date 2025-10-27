from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.personal_details import PersonalDetails
from models.user import User

personal_bp = Blueprint('personal_bp', __name__)

@personal_bp.route('/me/details', methods=['POST', 'PUT'])
@jwt_required()
def add_or_update_details():
    user_id = get_jwt_identity()
    data = request.get_json()
    valid_keys = {'weight','height','gender'}
    if not any(k in data for k in valid_keys):
        return jsonify({"error":"Missing personal details"}),400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"User not found"}),404

    details = PersonalDetails.query.filter_by(user_id=user_id).first()
    if details:
        details.weight = data.get('weight', details.weight)
        details.height = data.get('height', details.height)
        details.gender = data.get('gender', details.gender)
    else:
        details = PersonalDetails(user_id=user_id, weight=data.get('weight'), height=data.get('height'), gender=data.get('gender'))
        db.session.add(details)
    db.session.commit()
    return jsonify({"message":"Personal details saved","details":{"id":details.id,"user_id":details.user_id,"weight":details.weight,"height":details.height,"gender":details.gender}}),200

@personal_bp.route('/me/details', methods=['GET'])
@jwt_required()
def get_details():
    user_id = get_jwt_identity()
    details = PersonalDetails.query.filter_by(user_id=user_id).first()
    if not details:
        return jsonify({"message":"No personal details found"}),404
    return jsonify({"id":details.id,"user_id":details.user_id,"weight":details.weight,"height":details.height,"gender":details.gender})
