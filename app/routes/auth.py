from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.models import Member


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Missing email or password'}), 400

    member = Member.query.filter_by(email=email).first()
    if not member or not check_password_hash(member.password, password):
        return jsonify({'msg': 'Invalid email or password'}), 401

    print("Member >>>>>>>>>>>>>>>>>>>>>>>>", member.id)
    access_token = create_access_token(identity=str(member.id))
    return jsonify(access_token=access_token), 200
