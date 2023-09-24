from flask_restx import Namespace
from app import limiter, api_models
from flask_restx import Resource
from flask import session
from . import auth
from . import db
import json

licse_auth_ns = Namespace('auth')
login_model = licse_auth_ns.model('Login', api_models.login_model)
register_model = licse_auth_ns.model('Register', api_models.register_model)

@licse_auth_ns.route('/login')
class LoginUser(Resource):
    @licse_auth_ns.expect(login_model)
    @limiter.limit("10 per minute")
    def post(self):
        user_data = licse_auth_ns.payload
        email = user_data['email']
        password = user_data['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            return {'error': str(e)}, 400
        
        user_id = user['localId']
        user_token = user['idToken']

        session['currentId'] = user_id
        session['currentToken'] = user_token

        try:
            got_userdata = db.child("users").child(user_id).get(user_token)
            got_userdata = got_userdata.val()
        except Exception as e:
            return {'message': 'Falha ao obter os dados do usuário: ' + str(e)}, 400

        return {'userData':got_userdata, 'token': user_token}, 200

@licse_auth_ns.route('/register')
class RegisterUser(Resource):
    @licse_auth_ns.expect(register_model)
    @limiter.limit("1 per minute")
    def post(self):
        data = licse_auth_ns.payload
        email = data['email']
        password = data['password']
        fullname = data['fullname']
        favcolor = data['favcolor']
        age = data['age']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            
        except Exception as e:
            return {'message': 'Falha ao registrar usuário: ' + str(e)}, 400
        
        user_id = user['localId']
        user_token = user['idToken']

        session['currentId'] = user_id
        session['currentToken'] = user_token

        user_data = {
            "fullName": fullname,
            "favColor": favcolor,
            "age": age
        }

        try:
            db.child("users").child(user_id).set(user_data, user_token)
            return {'message': 'Usuário registrado com êxito!'}, 200
        except Exception as e:
            return {'message': f'Usuário criado! Porém... Erro ao registrar os dados dele: {str(e)}'}, 500

@licse_auth_ns.route("/logout")
class Logout(Resource):
    def post(self):
        session.pop("currentId", None)
        session.pop("currentToken", None)
        return {"message": "Logout successful"}, 200

