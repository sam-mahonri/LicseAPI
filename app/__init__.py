from flask import Flask
from .extensions import api
from .resources import licse_auth_ns, licse_status_ns, licse_chat_ns, licse_root_ns
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['DEBUG'] = os.getenv("LICSE_DEBUG")
    app.config['ENV'] = os.getenv("LICSE_ENV")

    api.init_app(app)

    api.add_namespace(licse_status_ns)
    api.add_namespace(licse_auth_ns)
    api.add_namespace(licse_chat_ns)
    api.add_namespace(licse_root_ns)

    return app
