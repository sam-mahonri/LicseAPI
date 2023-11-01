from flask_restx import Namespace
licse_ai_ns = Namespace('licseai')

from .licseglue import WikipediaSummarizer

from app import limiter, api_models
from flask_restx import Resource
from flask import session
import json
import requests

from .licseglue import summarize

from . import licse_keyword_extraction

sayHi_model = licse_ai_ns.model('[Test] Keyword Extraction', api_models.sayhi_model)
letsChat_model = licse_ai_ns.model('Chat with Licse', api_models.letsChat_model)


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

@licse_ai_ns.route('/licse')
class Licse(Resource):
    @limiter.limit('50 per minute')
    @licse_ai_ns.expect(letsChat_model)
    def get(self):
        data = licse_ai_ns.payload
        type_chat = data['type']
        text = data['prompt']

        if len(text) > 36210:
            return {'licseError':'LIMIT_CHAR', 'message': 'Você excedeu a quantidade de caracteres! o limite é de 36210'}, 429

        if type_chat == 'WEB':
            try:
                summarizer = WikipediaSummarizer()
                search_query = text
                search_keyword = summarizer.extract_keyword(search_query)

                if not search_keyword:
                    search_keyword = search_query.split()[0]
                print("summaWeb: " + search_keyword)
                summary = summarizer.summarize_article(search_keyword)
                greeting = f"Olá! Aqui está um resumo sobre '{search_keyword}':\n\n"
                
                saida = ''
                if summary:
                    saida = greeting + summary
                else:
                    saida = f"Artigo contendo a palavra-chave '{search_keyword}' não encontrado na Wikipedia em português."

                return {'licse': saida}
            except:
                return {'licse': "Não posso prosseguir, ocorreu alguma falha ao realizar a minha pesquisa, tente novamente mais tarde..."}
        elif type_chat == 'SUMMARIZE':
            #try:

            print("summa: " + text)
            summary = summarize.summarize_article(text)
            
            saida = ''
            if summary:
                if len(summary) < 30:
                    saida = "Hmmm, tente um texto maior, aparentemente este texto já está resumido, me mande um artigo inteiro e grande..."
                else:
                    saida = summary
            else:
                saida = "... Não consegui resumir, aparentemente este texto ainda é pequeno demais..."

            return {'licse': saida}
           # except:
                #return {'licse': "Não posso prosseguir, ocorreu alguma falha ao realizar o resumo, tente novamente mais tarde..."}
        else:
            return {'licse':"Hmm... Não sei o que responder."}
