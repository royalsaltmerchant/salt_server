from flask import request, Blueprint, Response, jsonify, current_app
from salt import db, bcrypt
from salt.models import User
from salt.serializers import UserSchema
from salt.users.utils import send_reset_email, send_update_coins_email
from functools import wraps
import logging, json
import jwt
import datetime
import os

users = Blueprint('users', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users.route('/api/register', methods=['POST'])
def api_register():
    data = json.loads(request.data)
    username = data['username']
    email = data['email'].lower()
    first_name = data['first_name'].lower()
    last_name = data['last_name'].lower()
    admin = data['admin'] if 'admin' in data else False
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(username=username, email=email, first_name=first_name, last_name=last_name, admin=admin, password=hashed_password)
    if user:
        db.session.add(user)
        db.session.commit()

        user_serialized = user_schema.dump(user)
        response = Response(
            response=json.dumps(user_serialized),
            status=201,
            mimetype='application/json'
        )
        return response
    else :
        return Response(
        response='Incorrect account information',
        status=400
        )

@users.route('/api/login', methods=['GET', 'POST'])
def api_login():
    data = json.loads(request.data)
    username = data['username_or_email']
    email = data['username_or_email'].lower()
    user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(hours=168)
            }
        token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")

        response = Response(
            response=json.dumps({'token': token}),
            status=200,
            mimetype='application/json'
    )
        return response
    else:
        return Response(
            response='Incorrect account information',
            status=400
        )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers["x-access-token"] != "null":
            req_token = request.headers["x-access-token"]
            token_split = req_token.split(' ')
            token = token_split[1]
            try:
                verification = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = db.session.query(User).filter_by(id=verification['user_id']).first()
            except:
                return jsonify({'message': 'Invalid token or user'})

        else:
            return Response(
            response='No token passed',
            status=400
        )

        return f(current_user, *args, **kwargs)
    return decorated

@users.route('/api/verify_jwt', methods=['GET', 'POST'])
def api_verify_jwt():
    token = None

    if 'x-access-token' in request.headers:
        req_token = request.headers["x-access-token"]
        token_split = req_token.split(' ')
        token = token_split[1]

    if not token:
        return Response(
            response='No token passed',
            status=400
        )
    else:
        verification = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
        current_user = db.session.query(User).filter_by(id=verification['user_id']).first()
        user_serialized = user_schema.dump(current_user)
        return Response(
            response=json.dumps(user_serialized),
            status=200,
            mimetype='application/json'
        )

@users.route('/api/get_user', methods=['GET', 'POST'])
@token_required
def get_user(current_user):
    user_serialized = user_schema.dump(current_user)
    return Response(
        response=json.dumps(user_serialized),
        status=200,
        mimetype='application/json'
    )

@users.route('/api/get_user_by_username', methods=['GET', 'POST'])
def get_user_by_username():
    data = json.loads(request.data)
    username = data['username']
    user = db.session.query(User).filter_by(username=username).first()
    user_serialized = user_schema.dump(user)
    return Response(
        response=json.dumps(user_serialized),
        status=200,
        mimetype='application/json'
    )

@users.route('/api/users', methods=['GET', 'POST'])
def get_users():
    users = db.session.query(User).all()
    users_serialized = users_schema.dump(users)
    return Response(
        response=json.dumps(users_serialized),
        status=200,
        mimetype='application/json'
    )

@users.route('/api/edit_user', methods={'POST'})
@token_required
def edit_user(current_user):
    data = json.loads(request.data)
    user_id = data['user_id']
    user_to_edit = db.session.query(User).filter_by(id=user_id).first()
    if 'email' in data:
        user_to_edit.email = data['email'].lower()
    if 'username' in data:
        user_to_edit.username = data['username']
    if 'approved_asset_count' in data:
        user_to_edit.approved_asset_count = user_to_edit.approved_asset_count + data['approved_asset_count']
    if 'coins' in data:
        user_to_edit.coins = user_to_edit.coins + data['coins']
        # send coins email
        # send_update_coins_email(user_to_edit, user_to_edit.coins)
    if 'premium' in data:
        user_to_edit.premium = data['premium']
    if 'upload_count' in data:
        user_to_edit.upload_count = data['upload_count']
    if 'about' in data:
        user_to_edit.about = data['about']
    if 'address' in data:
        user_to_edit.address = data['address']
    if 'phone' in data:
        user_to_edit.phone = data['phone']
        
    db.session.commit()
    user_serialized = user_schema.dump(user_to_edit)

    return Response(
        response=json.dumps(user_serialized),
        status=200,
        mimetype='application/json'
    )

@users.route('/api/request_reset_email', methods=['POST'])
def request_reset_email():
    data = json.loads(request.data)
    email = data['email'].lower()
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return Response(
            response='no user found by this email',
            status=400
        )
    else:
        send_reset_email(user)
        return Response(
            response='Email has been sent!',
            status=200
    )

@users.route('/api/reset_password', methods=['POST'])
def api_reset_token():
    data = json.loads(request.data)
    token = data['token']
    user = User.verify_reset_token(token)
    if user is None:
        return Response(
            response='That is an invalid or expired token',
            status=400
        )
    else: 
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        user_serialized = user_schema.dump(user)

        return Response(
            response=json.dumps(user_serialized),
            status=200,
            mimetype='application/json'
        )