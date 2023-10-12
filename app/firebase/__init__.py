
from app.db_config import get_config, get_firebaseapi
import pyrebase, requests

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

from . import auth
from . import db