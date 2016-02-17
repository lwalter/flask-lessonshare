from datetime import datetime
from flask import Blueprint, jsonify, request
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError
from config import Config
from .models import Users


user_auth = Blueprint("user_auth", __name__)


def authenticate(email, password):
    user = Users.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return None

    return user


def identity(payload):
    user_id = payload['identity']
    user = Users.query.get(user_id)

    if not user:
        return None

    return user


def payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + Config.JWT_EXPIRATION_DELTA
    nbf = iat + Config.JWT_NOT_BEFORE_DELTA
    identity_id = getattr(identity, 'id') or identity['id']
    identity_firstname = getattr(identity, 'first_name') or identity['first_name']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity_id, 'first_name': identity_firstname}


@user_auth.route('/api/user/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    if not email or not password:
        return jsonify({'description': 'Invalid credentials.'}), 400

    user = Users.query.filter_by(email=request.json['email']).first()

    if not user or not user.verify_password(password):
        return jsonify({'description': 'Invalid credentials.'}), 401

    auth_token = user.generate_auth_token()
    return jsonify({'token': auth_token.decode('ascii')}), 200


class UserApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('first_name', type=str, required=True, help='No first name provided', location='json')
        self.reqparse.add_argument('last_name', type=str, required=True, help='No last name provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')

        super(self.__class__, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        new_user = Users(email=args.get('email'),
                         first_name=args.get('first_name'),
                         last_name=args.get('last_name'),
                         password=args.get('password'))

        try:
            new_user.save()
        except IntegrityError, e:
            return {'description': 'User with given email already exists.'}, 409
        except Exception, e:
            return {'description': 'Server encountered an error.'}, 500

        return {'first_name': new_user.first_name}, 201
