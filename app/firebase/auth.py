from flask_restx import Namespace
from app import limiter, api_models
from app.db_config import get_firebaseapi
from flask_restx import Resource
from . import auth, db, get_user_info
import json
import requests

licse_auth_ns = Namespace('auth')
login_model = licse_auth_ns.model('Login', api_models.login_model)
register_model = licse_auth_ns.model('Register', api_models.register_model)
send_email_model = licse_auth_ns.model('Send email', api_models.send_email_ver)


@licse_auth_ns.route('/login')
class LoginUser(Resource):
    @licse_auth_ns.expect(login_model)
    @limiter.limit("50 per minute")
    def post(self):
        user_data = licse_auth_ns.payload
        email = user_data['email']
        password = user_data['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print(e)
            return {'error': str(e)}, 400
        
        user_id = user['localId']
        user_token = user['idToken']

        return {'token': user_token, 'userId': user_id}, 200

@licse_auth_ns.route('/register')
class RegisterUser(Resource):
    @licse_auth_ns.expect(register_model)
    @limiter.limit("10 per minute")
    def post(self):
        data = licse_auth_ns.payload
        email = data['email']
        password = data['password']
        fullname = data['fullName']
        favcolor = data['favColor']
        age = data['age']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            
        except Exception as e:
            return {'licseError':'ERROR_REGISTER_USER', 'message': 'Falha ao registrar usuário: ' + str(e)}, 400
        
        user_id = user['localId']
        user_token = user['idToken']

        user_data = {
            "fullName": fullname,
            "favColor": favcolor,
            "age": age,
            "points":0,
            "redflags":0
        }

        try:
            db.child("users").child(user_id).set(user_data, user_token)
            return {'licseError':'SUCCESS_REGISTER_USER', 'message': 'Usuário registrado com êxito!', 'token': user_token, 'userId':user_id}, 200
        except Exception as e:
            return {'licseError':'ERROR_REGISTER_USER_INFO', 'message': f'Usuário criado! Porém... Erro ao registrar os dados dele: {str(e)}'}, 500


@licse_auth_ns.route("/send_email_verification")
class sendEmailVerification(Resource):
    @limiter.limit("15 per minute")
    @licse_auth_ns.expect(send_email_model)
    def post(self):
        data = licse_auth_ns.payload

        currentToken = data['token']
        dbApi = get_firebaseapi()

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={dbApi}"
        headers = {'Content-Type': 'application/json'}
        data = {"requestType": "VERIFY_EMAIL", "idToken": currentToken}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return {'licseError':'SUCCESS_SEND_EMAIL_VERIFICATION', 'message': "Email de verificação enviado!"}, 200
        else:
            return {'licseError':'ERROR_SEND_EMAIL_VERIFICATION', 'message': "Moiô, email de verificação não enviado..."}, 500
        
@licse_auth_ns.route("/email_verified")
class emailVerified(Resource):
    @limiter.limit("20 per minute")
    @licse_auth_ns.expect(send_email_model)
    def post(self):
        data = licse_auth_ns.payload

        currentToken = data['token']
        user_info = get_user_info(currentToken)
        return user_info['emailVerified']
    
@licse_auth_ns.route("/delete_user")
class deleteUser(Resource):
    @limiter.limit("50 per minute")
    @licse_auth_ns.expect(send_email_model)
    def delete(self):
        data = licse_auth_ns.payload

        currentToken = data['token']
        currentId = data['userId']

        try:
            db.child("users").child(currentId).remove(currentToken)
            auth.delete_user_account(currentToken)
            return {'licseError':'SUCCESS_DELETE_USER_REGISTER', 'message': "Usuário removido com êxito!"}, 200
        except Exception as e:
            return {'licseError':'ERROR_DELETE_USER_REGISTER', 'message': f'Problema ao deletar usuário: {str(e)}'}, 500