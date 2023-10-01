
from app.db_config import get_config, get_firebaseapi
import pyrebase, requests
from flask import session

pb_set = get_config()
firebase = pyrebase.initialize_app(pb_set)

auth = firebase.auth()
db = firebase.database()

def get_user_info(currentToken):
    firebase_api = get_firebaseapi()

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={firebase_api}"
    headers = {'Content-Type': 'application/json'}
    data = {"idToken": currentToken}
    response = requests.post(url, headers=headers, json=data)
    user_info = response.json()['users'][0]

    return user_info

def verify_current_user():
    if not "currentToken" in session or not "currentId" in session:
        return False

    currentToken = session['currentToken']

    data = firebase.get_user_info(currentToken)

    return data['emailVerified']

def get_status_user_info():
    if not "currentToken" in session or not "currentId" in session:
        return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

    currentToken = session['currentToken']
    currentId = session['currentId']

    return {"cT":currentToken, "cI":currentId}

from . import auth
from . import db