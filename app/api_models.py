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

### CRUD ###

# C
dbCreateChat_model = {
    'title': fields.String(required=True, description='Título do novo chat a ser criado')
}

dbCreateMessage_model = {
    'chatId': fields.String(required=True, description='ID do chat onde está a mensagem'),
    'sender': fields.String(required=True, description='Quem enviou a mensagem? [you, licse]'),
    'message': fields.String(required=True, description='A mensagem em si')
}

# R
dbReadChat_model = {
    'chatId': fields.String(required=True, description="ID do chat")
}

# U
dbUpdateUser_model = {
    'data': fields.Raw(required=True, description='Dado(s) a ser(em) atualizado(s) em dicionario ou apenas String caso uma mensagem esteja sendo editada, por exemplo: {favColor:"#e62169"} ou aninhar mais chaves permitidas ao mesmo tempo, por exemplo: {"favColor":"....", "fullName":"...."}. Não se preocupe com as permissões, o usuário logado na sessão já carregará o Token e ID.')
}

dbUpdateChatTitle_model = {
    'newTitle': fields.String(required=True, description="Novo título do chat"),
    'chatId': fields.String(required=True, description="ID do chat"),
}

# D

dbDeleteChat_model = {
    'chatId': fields.String(required=True, description="ID do chat")
}

### CRUD ###

post_model = {
    'id': fields.Integer(readonly=True, description='ID da postagem'),
    'title': fields.String(required=True, description='Título da postagem'),
    'content': fields.String(required=True, description='Conteúdo da postagem'),
    'author_id': fields.Integer(required=True, description='ID do autor da postagem'),
}

comment_model = {
    'id': fields.Integer(readonly=True, description='ID do comentário'),
    'text': fields.String(required=True, description='Texto do comentário'),
    'post_id': fields.Integer(required=True, description='ID da postagem associada'),
    'user_id': fields.Integer(required=True, description='ID do usuário que fez o comentário'),
}

allowed_user_keys = {
    "fullName",
    "favColor",
    "age",
    "chats"
}