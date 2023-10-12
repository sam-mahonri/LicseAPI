from flask_restx import fields

login_model = {
    'email': fields.String(required=True, description='Endereço de e-mail do usuário'),
    'password': fields.String(required=True, description='Senha do usuário'),
}

register_model = {
    'email': fields.String(required=True, description='Endereço de e-mail do usuário'),
    'password': fields.String(required=True, description='Senha do usuário'),
    'fullName': fields.String(required=True, description='Nome completo do usuário'),
    'favColor': fields.String(required=True, description='Cor do tema do usuário em HEX - Ex: #e62169 (Vermelho)'),
    'age': fields.Integer(required=True, description='Idade atual do novo usuário')
}

send_email_ver = {
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=False, description='ID do usuário logado')
}

### CRUD ###

# C
dbCreateChat_model = {
    'title': fields.String(required=True, description='Título do novo chat a ser criado'),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

dbCreateMessage_model = {
    'chatId': fields.String(required=True, description='ID do chat onde está a mensagem'),
    'sender': fields.String(required=True, description='Quem enviou a mensagem? [you, licse]'),
    'message': fields.String(required=True, description='A mensagem em si'),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

# R
dbReadChat_model = {
    'chatId': fields.String(required=True, description="ID do chat"),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

# U
dbUpdateUser_model = {
    'data': fields.Raw(required=True, description='Dado(s) a ser(em) atualizado(s) em dicionario ou apenas String caso uma mensagem esteja sendo editada, por exemplo: {favColor:"#e62169"} ou aninhar mais chaves permitidas ao mesmo tempo, por exemplo: {"favColor":"....", "fullName":"...."}. Não se preocupe com as permissões, o usuário logado na sessão já carregará o Token e ID.'),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')

}

dbUpdateChatTitle_model = {
    'newTitle': fields.String(required=True, description="Novo título do chat"),
    'chatId': fields.String(required=True, description="ID do chat"),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

# D

dbDeleteChat_model = {
    'chatId': fields.String(required=True, description="ID do chat"),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

### Licse AI ###

sayhi_model = {
    'prompt': fields.String(required=True, description="Mensagem a ser enviada para o Licse You"),
    'token': fields.String(required=True, description='Token do usuário logado'),
    'userId': fields.String(required=True, description='ID do usuário logado')
}

allowed_user_keys = {
    "fullName",
    "favColor",
    "age",
    "chats"
}