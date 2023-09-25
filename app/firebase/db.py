from flask_restx import Namespace
from app import limiter, api_models
from app.db_config import get_timezone, get_firebaseapi
from flask_restx import Resource
from flask import session
import datetime, pytz, requests
from . import auth, db, get_user_info

licse_db_ns = Namespace('licsedb')
updateUser_model = licse_db_ns.model('Update User in DB', api_models.dbUpdateUser_model)

createChat_model = licse_db_ns.model('Create chat in DB', api_models.dbCreateChat_model)
createMessage_model = licse_db_ns.model('Create message in chat', api_models.dbCreateMessage_model)
readChat_model = licse_db_ns.model('Read chat in DB', api_models.dbReadChat_model)
updateChatTitle_model = licse_db_ns.model('Update chat title in DB', api_models.dbUpdateChatTitle_model)
deleteChat_model = licse_db_ns.model('Delete chat in DB', api_models.dbDeleteChat_model)

@licse_db_ns.route('/user/read')
class ReadUser(Resource):
    @limiter.limit("50 per minute")
    def get(self):

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            gotData = db.child("users").child(currentId).get(currentToken)
            gotData = gotData.val()
            return {"gotData": gotData}, 200
        except Exception as e:
            return {'licseError':'ERROR_READ_USER', 'message': f'Erro ao ler o(s) dado(s): {str(e)}'}, 500

@licse_db_ns.route('/user/update')
class UpdateUser(Resource):
    @licse_db_ns.expect(updateUser_model)
    @limiter.limit("50 per minute")
    def put(self):
        user_data = licse_db_ns.payload

        if not set(user_data['data'].keys()) <= api_models.allowed_user_keys:
            return {'licseError':'DENIED_KEYS', 'message': 'Tem certeza que esse dicionario possui uma chave válida? Verifique se a(s) chave(s) que você está tentando atualizar estão dentro do escopo de variáveis aceitas!'}, 401

        data = user_data['data']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
                
        try:
            db.child("users").child(currentId).update(data, currentToken)
            return {'licseError':'SUCCESS_USER_UPDATED', 'message': 'Dado(s) atualizado(s) com êxito!'}, 200
        except Exception as e:
            return {'licseError':'ERROR_USER_UPDATED', 'message': f'Erro ao atualizar o(s) dado(s): {str(e)}'}, 500

@licse_db_ns.route('/chats/create')
class CreateChat(Resource):
    @licse_db_ns.expect(createChat_model)
    @limiter.limit("2 per minute")
    def post(self):
        chat_data = licse_db_ns.payload
        newChat_title = chat_data['title']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        user_info = get_user_info(currentToken)

        if not user_info['emailVerified']:
            return {'licseError':'NON_VERIFIED_EMAIL', 'message': 'Email não verificado! Você não pode continuar assim! chame "/send_email_verification" e tente novamente'}, 429

        cur_timezone = get_timezone()

        brasilia_tz = pytz.timezone(cur_timezone)

        now = datetime.datetime.now(brasilia_tz)
        now_iso = now.isoformat() + 'Z'

        chatStruct = {
            'chatTitle':newChat_title,
            'messages':[],
            "datetime":now_iso
        }

        try:
            db.child("users").child(currentId).child('chats').push(chatStruct, currentToken)
            return {'licseError':'SUCCESS_CREATE_CHAT', 'message': 'Chat criado com êxito!'}, 200
        except Exception as e:
            return {'licseError':'ERROR_CREATE_CHAT', 'message': f'Erro ao criar o chat: {str(e)}'}, 500

@licse_db_ns.route('/chats/updatetitle')
class UpdateChat(Resource):
    @licse_db_ns.expect(updateChatTitle_model)
    @limiter.limit("10 per minute")
    def put(self):
        chat_data = licse_db_ns.payload
        newChat_title = chat_data['newTitle']
        chatId_title = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        user_info = get_user_info(currentToken)

        if not user_info['emailVerified']:
            return {'licseError':'NON_VERIFIED_EMAIL', 'message': 'Email não verificado! Você não pode continuar assim! chame "/send_email_verification" e tente novamente'}, 429

        try:
            db.child("users").child(currentId).child('chats').child(chatId_title).update({'chatTitle':newChat_title}, currentToken)
            return {'licseError':'SUCCESS_CHAT_TITLE_UPDATE', 'message': 'Título atualizado com êxito'}, 200
        except Exception as e:
            return {'licseError':'ERROR_CHAT_TITLE_UPDATE', 'message': f'Erro ao editar o título: {str(e)}'}, 500

@licse_db_ns.route('/chats/delete')
class DeleteChat(Resource):
    @licse_db_ns.expect(deleteChat_model)
    @limiter.limit("50 per minute")
    def delete(self):
        chat_data = licse_db_ns.payload

        chat = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        user_info = get_user_info(currentToken)

        if not user_info['emailVerified']:
            return {'licseError':'NON_VERIFIED_EMAIL', 'message': 'Email não verificado! Você não pode continuar assim! chame "/send_email_verification" e tente novamente'}, 429

        try:
            db.child("users").child(currentId).child('chats').child(chat).remove(currentToken)
            return {'licseError':'SUCCESS_CHAT_DELETE', 'message': 'Conversa removida com êxito'}, 200
        except Exception as e:
            return {'licseError':'ERROR_CHAT_DELETE', 'message': f'Erro ao remover a conversa: {str(e)}'}, 500
        
@licse_db_ns.route('/chats/read')
class ReadChat(Resource):
    @licse_db_ns.expect(readChat_model)
    @limiter.limit("50 per minute")
    def get(self):
        chat_data = licse_db_ns.payload

        chatId = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        user_info = get_user_info(currentToken)

        if not user_info['emailVerified']:
            return {'licseError':'NON_VERIFIED_EMAIL', 'message': 'Email não verificado! Você não pode continuar assim! chame "/send_email_verification" e tente novamente'}, 429

        try:
            gotData = db.child("users").child(currentId).child('chats').child(chatId).get(currentToken)
            gotData = gotData.val()
            return {"gotData": gotData}, 200
        except Exception as e:
            return {'licseError':'ERROR_CHAT_READ', 'message': f'Erro ao ler o chat: {str(e)}'}, 500
        
@licse_db_ns.route('/chats/addmsg')
class AddMessage(Resource):
    @licse_db_ns.expect(createMessage_model)
    @limiter.limit("5 per minute")
    def post(self):
        chat_data = licse_db_ns.payload
        chatId = chat_data['chatId']
        sender = chat_data['sender']
        message = chat_data['message']

        if not "currentToken" in session or not "currentId" in session:
            return {'licseError':'NO_USER_LOGGEDIN', 'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        cur_timezone = get_timezone()

        brasilia_tz = pytz.timezone(cur_timezone)

        now = datetime.datetime.now(brasilia_tz)
        now_iso = now.isoformat() + 'Z'

        chatStruct = {
            'sender':sender,
            'message':message,
            'timestamp':now_iso
        }

        try:
            db.child("users").child(currentId).child('chats').child(chatId).child('messages').push(chatStruct, currentToken)
            return {'licseError':'SUCCESS_MSG_SAVED', 'message': 'Mensagem salva com êxito'}, 200
        except Exception as e:
            return {'licseError':'ERROR_MSG_SAVED', 'message': f'Erro ao salvar a mensagem: {str(e)}'}, 500
