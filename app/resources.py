from dotenv import load_dotenv, find_dotenv
from flask import send_file, jsonify
from flask_restx import Resource, Namespace
from app import limiter
import os

licse_status_ns = Namespace('about', __name__="status")
licse_chat_ns = Namespace('chat')
licse_root_ns = Namespace('/')

@licse_status_ns.route('/')
class AboutLicse(Resource):
    @limiter.limit("5 per minute")
    def get(self):
        return jsonify([load_dotenv(), find_dotenv(), os.getcwd(), os.path.isfile(find_dotenv())])
@licse_root_ns.route('/favicon.ico')
class FavIcon(Resource):
    def get(self):
        return send_file('./static/source/logos/favicon.ico')
    
@licse_root_ns.route('/swaggerui/favicon-32x32.png')
@licse_root_ns.route('/swaggerui/favicon-16x16.png')
class FavIcon32(Resource):
    def get(self):
        return send_file('./static/source/logos/favicon.ico')

@licse_root_ns.route('/swaggerui/swagger-ui.css')
class SwaggerStyle(Resource):
    def get(self):
        return send_file('./static/styles/swgr.css')

@licse_root_ns.route('/backgrounddev')
class SwaggerBack(Resource):
    def get(self):
        return send_file('./static/source/backgrounds/background.svg')