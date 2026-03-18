from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from src.modules.users.models import db, User, Profile
from src.modules.users.services import token_required, create_token, login_google

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data: return jsonify({'message': 'Thiếu dữ liệu'}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username:
        return jsonify({'message': 'username bị bỏ trống.'}), 400

    if not password:
        return jsonify({'message': 'password bị bỏ trống.'}), 400

    if not email:
        return jsonify({'message': 'Email bị bỏ trống.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User đã tồn tại'}), 400


    new_user = User(username=username, password=password, email=email)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Đăng ký thành công'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username:
        return jsonify({'message': 'username bị trống.'}), 400
    if not password:
        return jsonify({'message': 'password bị trống.'}), 400

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({'message': 'Sai username hoặc password'}), 401

    token = create_token(user.id)
    return jsonify({'token': token})

@api.route('/login/google', methods=['POST'])
def login_google_api():
    data = request.get_json()

    token, error = login_google(data.get("token"))

    if error:
        return jsonify({"message": error}), 401

    return jsonify({"token": token})

@api.route('/protected')
@token_required
def protected(current_user):
    return jsonify({'message': f'Xin chào {current_user.username}, bạn đã qua xác thực!'})

@api.route('/profile', methods=['GET'])
@token_required
def get_profile():
    user_id = get_jwt_identity()

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return {"message": "Profile không tồn tại"}, 404

    return {
        "address": profile.address,
        "birthday": profile.birthday,
        "phone": profile.phone,
        "idenfication": profile.idenfication,
        "avatar": profile.avatar,
        "updated_date": profile.updated_date
    }
