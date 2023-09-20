from flask_restx import Resource, Namespace
from flask import send_file
from dotenv import load_dotenv
import os

licse_status_ns = Namespace('about')
licse_auth_ns = Namespace('auth')
licse_chat_ns = Namespace('chat')
licse_root_ns = Namespace('/')

@licse_status_ns.route('/')
class AboutLicse(Resource):
    def get(self):
        load_dotenv()
        return os.getenv('LICSE_VER')

@licse_root_ns.route('/favicon.ico')
class FavIcon(Resource):
    def get(self):
        return send_file('./static/source/logos/favicon.ico')