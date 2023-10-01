from flask_restx import Namespace
from app import limiter, api_models
from app.db_config import get_firebaseapi
from flask_restx import Resource
from flask import session
from . import auth, db, get_user_info
import json
import requests

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

        return {'token': user_token}, 200

@licse_auth_ns.route('/register')
class RegisterUser(Resource):
    @licse_auth_ns.expect(register_model)
    @limiter.limit("1 per minute")
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

        session['currentId'] = user_id
        session['currentToken'] = user_token

        user_data = {
            "fullName": fullname,
            "favColor": favcolor,
            "age": age,
            "points":0,
            "redflags":0
        }

        try:
            db.child("users").child(user_id).set(user_data, user_token)
            return {'licseError':'SUCCESS_REGISTER_USER', 'message': 'Usuário registrado com êxito!'}, 200
        except Exception as e:
            return {'licseError':'ERROR_REGISTER_USER_INFO', 'message': f'Usuário criado! Porém... Erro ao registrar os dados dele: {str(e)}'}, 500

@licse_auth_ns.route("/logout")
class Logout(Resource):
    def post(self):
        session.pop("currentId", None)
        session.pop("currentToken", None)
        return {'licseError':'SUCCESS_LOGOUT', 'message': "Logout successful"}, 200

@licse_auth_ns.route("/send_email_verification")
class sendEmailVerification(Resource):
    @limiter.limit("3 per minute")
    def post(self):

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
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
    @limiter.limit("10 per minute")
    def get(self):
        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        user_info = get_user_info(currentToken)
        return user_info['emailVerified']
    
@licse_auth_ns.route("/delete_user")
class deleteUser(Resource):
    def delete(self):
        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        try:
            db.child("users").child(currentId).remove(currentToken)
            auth.delete_user_account(currentToken)
            return {'licseError':'SUCCESS_DELETE_USER_REGISTER', 'message': "Usuário removido com êxito!"}, 200
        except Exception as e:
            return {'licseError':'ERROR_DELETE_USER_REGISTER', 'message': f'Problema ao deletar usuário: {str(e)}'}, 500