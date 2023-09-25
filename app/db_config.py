from dotenv import load_dotenv, find_dotenv
import os

def get_config():
    load_dotenv(find_dotenv())

    pb_config = {
        "apiKey": os.getenv('LICSE_FIREBASE_API_KEY'),
        "authDomain": os.getenv('LICSE_FIREBASE_AUTH_URL'),
        "projectId": os.getenv('LICSE_FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('LICSE_FIREBASE_STORAGE_BUCKET_URL'),
        "messagingSenderId": os.getenv('LICSE_FIREBASE_MESSAGE_ID'),
        "appId": os.getenv('LICSE_FIREBASE_API_ID'),
        "databaseURL": os.getenv('LICSE_FIREBASE_RTDB_URL')
    }

    return pb_config

def get_timezone():
    load_dotenv(find_dotenv())
    return os.getenv('LICSE_TIMEZONE')

def get_hostname():
    load_dotenv(find_dotenv())
    return os.getenv('LICSE_HOSTNAME')

def get_firebaseapi():
    load_dotenv(find_dotenv())
    return os.getenv('LICSE_FIREBASE_API_KEY')