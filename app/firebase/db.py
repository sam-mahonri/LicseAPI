from flask_restx import Namespace
from app import limiter, api_models
from app.db_config import get_timezone
from flask_restx import Resource
from flask import session
import datetime
import pytz
from . import db

licse_db_ns = Namespace('licsedb')
createUser_model = licse_db_ns.model('Create User in DB', api_models.dbCreateUser_model)
readUser_model = licse_db_ns.model('Read User in DB', api_models.dbReadUser_model)
updateUser_model = licse_db_ns.model('Update User in DB', api_models.dbUpdateUser_model)
deleteUser_model = licse_db_ns.model('Delete User in DB', api_models.dbDeleteUser_model)

createChat_model = licse_db_ns.model('Create chat in DB', api_models.dbCreateChat_model)
createMessage_model = licse_db_ns.model('Create message in chat', api_models.dbCreateMessage_model)
readChat_model = licse_db_ns.model('Read chat in DB', api_models.dbReadChat_model)
updateChatTitle_model = licse_db_ns.model('Update chat title in DB', api_models.dbUpdateChatTitle_model)
deleteChat_model = licse_db_ns.model('Delete chat in DB', api_models.dbDeleteChat_model)

@licse_db_ns.route('/user/create')
class CreateUser(Resource):
    @licse_db_ns.expect(createUser_model)
    @limiter.limit("50 per minute")
    def post(self):
        user_data = licse_db_ns.payload

        if not set(user_data['data'].keys()) <= api_models.allowed_user_keys:
            return {'message': 'Tem certeza que esse dicionario possui uma chave válida? Verifique se a(s) chave(s) que você está tentando atualizar estão dentro do escopo de variáveis aceitas!'}, 401

        data = user_data['data']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            db.child("users").child(currentId).set(data, currentToken)
            return {'message': 'Dado(s) criados(s) com êxito!'}, 200
        except Exception as e:
            return {'message': f'Erro ao criar o(s) dado(s): {str(e)}'}, 500

@licse_db_ns.route('/user/read')
class ReadUser(Resource):
    @licse_db_ns.expect(readUser_model)
    @limiter.limit("50 per minute")
    def get(self):
        user_data = licse_db_ns.payload

        key = user_data['key']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            gotData = db.child("users").child(currentId).child(key).get(currentToken)
            gotData = gotData.val()
            return {"gotData": gotData}, 200
        except Exception as e:
            return {'message': f'Erro ao ler o(s) dado(s): {str(e)}'}, 500

@licse_db_ns.route('/user/update')
class UpdateUser(Resource):
    @licse_db_ns.expect(updateUser_model)
    @limiter.limit("50 per minute")
    def put(self):
        user_data = licse_db_ns.payload

        if not set(user_data['data'].keys()) <= api_models.allowed_user_keys:
            return {'message': 'Tem certeza que esse dicionario possui uma chave válida? Verifique se a(s) chave(s) que você está tentando atualizar estão dentro do escopo de variáveis aceitas!'}, 401

        data = user_data['data']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
                
        try:
            db.child("users").child(currentId).update(data, currentToken)
            return {'message': 'Dado(s) atualizado(s) com êxito!'}, 200
        except Exception as e:
            return {'message': f'Erro ao atualizar o(s) dado(s): {str(e)}'}, 500

@licse_db_ns.route('/user/delete')
class DeleteUser(Resource):
    @licse_db_ns.expect(deleteUser_model)
    @limiter.limit("50 per minute")
    def delete(self):
        user_data = licse_db_ns.payload

        key = user_data['key']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            db.child("users").child(currentId).child(key).remove(currentToken)
            return {'message': 'Chave removida com êxito!'}, 200
        except Exception as e:
            return {'message': f'Erro ao remover a chave: {str(e)}'}, 500
        
@licse_db_ns.route('/chats/create')
class CreateChat(Resource):
    @licse_db_ns.expect(createChat_model)
    @limiter.limit("2 per minute")
    def post(self):
        chat_data = licse_db_ns.payload
        newChat_title = chat_data['title']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        chatStruct = {
            'chatTitle':newChat_title,
            'messages':[]
        }

        try:
            db.child("users").child(currentId).child('chats').push(chatStruct, currentToken)
            return {'message': 'Chat criado com êxito!'}, 200
        except Exception as e:
            return {'message': f'Erro ao criar o chat: {str(e)}'}, 500

@licse_db_ns.route('/chats/updatetitle')
class CreateChat(Resource):
    @licse_db_ns.expect(updateChatTitle_model)
    @limiter.limit("10 per minute")
    def put(self):
        chat_data = licse_db_ns.payload
        newChat_title = chat_data['newTitle']
        chatId_title = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']

        try:
            db.child("users").child(currentId).child('chats').child(chatId_title).update({'chatTitle':newChat_title}, currentToken)
            return {'message': 'Título atualizado com êxito'}, 200
        except Exception as e:
            return {'message': f'Erro ao editar o título: {str(e)}'}, 500

@licse_db_ns.route('/chats/delete')
class DeleteChat(Resource):
    @licse_db_ns.expect(deleteChat_model)
    @limiter.limit("50 per minute")
    def delete(self):
        chat_data = licse_db_ns.payload

        chat = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            db.child("users").child(currentId).child('chats').child(chat).remove(currentToken)
            return {'message': 'Conversa removida com êxito'}, 200
        except Exception as e:
            return {'message': f'Erro ao remover a conversa: {str(e)}'}, 500
        
@licse_db_ns.route('/chats/read')
class ReadChat(Resource):
    @licse_db_ns.expect(readChat_model)
    @limiter.limit("50 per minute")
    def get(self):
        chat_data = licse_db_ns.payload

        chatId = chat_data['chatId']

        if not "currentToken" in session or not "currentId" in session:
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

        currentToken = session['currentToken']
        currentId = session['currentId']
        
        try:
            gotData = db.child("users").child(currentId).child('chats').child(chatId).get(currentToken)
            gotData = gotData.val()
            return {"gotData": gotData}, 200
        except Exception as e:
            return {'message': f'Erro ao ler o chat: {str(e)}'}, 500
        
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
            return {'message': 'Nenhum usuário logado no momento! Faça login em "/login" antes de chamar esta rota!'}, 401

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
            return {'message': 'Mensagem salva com êxito'}, 200
        except Exception as e:
            return {'message': f'Erro ao salvar a mensagem: {str(e)}'}, 500
