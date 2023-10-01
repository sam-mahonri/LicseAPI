from flask_restx import Namespace
licse_ai_ns = Namespace('licseai')

from app import limiter, api_models
from flask_restx import Resource
from flask import session
import json
import requests

from . import licse_keyword_extraction

sayHi_model = licse_ai_ns.model('Chat with Licse', api_models.sayhi_model)

@licse_ai_ns.route('/sayhi')
class HiLicse(Resource):
    @limiter.limit('5 per minute')
    @licse_ai_ns.expect(sayHi_model)
    def post(self):
        data = licse_ai_ns.payload
        text = data['prompt']

        if len(text) > 2000:
            return {'licseError':'LIMIT_CHAR', 'message': 'Você excedeu a quantidade de caracteres! o limite é de 2000'}, 429

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        keywords = licse_keyword_extraction.get_keywords(text)
        return keywords