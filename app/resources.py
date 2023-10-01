from dotenv import load_dotenv, find_dotenv
from flask import send_file, jsonify, render_template, make_response
from flask_restx import Resource, Namespace
from app import limiter, about_licse
import os

licse_status_ns = Namespace('about', __name__="status")
licse_chat_ns = Namespace('chat')
licse_root_ns = Namespace('/')

@licse_status_ns.route('/')
class AboutLicse(Resource):
    @limiter.limit("5 per minute")
    def get(self):
        return jsonify(about_licse.about)
@licse_root_ns.route('/favicon.ico', doc=False)
class FavIcon(Resource):
    def get(self):
        return send_file('./static/source/logos/favicon.ico')
    
@licse_root_ns.route('/swaggerui/favicon-32x32.png', doc=False)
@licse_root_ns.route('/swaggerui/favicon-16x16.png', doc=False)
class FavIcon32(Resource):
    def get(self):
        return send_file('./static/source/logos/favicon.ico')

@licse_root_ns.route('/swaggerui/swagger-ui.css', doc=False)
class SwaggerStyle(Resource):
    def get(self):
        return send_file('./static/styles/swgr.css')

@licse_root_ns.route('/backgrounddev', doc=False)
class SwaggerBack(Resource):
    def get(self):
        return send_file('./static/source/backgrounds/background.png')
