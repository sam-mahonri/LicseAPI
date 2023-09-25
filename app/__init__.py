from flask import Flask, request, render_template
from dotenv import load_dotenv, find_dotenv
from flask_limiter import Limiter
from app.limiter_config import LIMITER_ENABLED, LIMITER_STORAGE_URI, LIMITER_KEY_FUNC
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import os
from . import about_licse

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

limiter = Limiter(
        LIMITER_KEY_FUNC,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=LIMITER_STORAGE_URI,
        enabled=LIMITER_ENABLED
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('home.html', version=about_licse.about["version"], versionCodename=about_licse.about["codename"], knowledge=about_licse.about["knowledge"], serverLocal=about_licse.about["university"]), 404

def create_app():

    from .resources import licse_status_ns, licse_chat_ns, licse_root_ns
    from .firebase.auth import licse_auth_ns
    from .firebase.db import licse_db_ns
    from .extensions import api

    load_dotenv(find_dotenv())
    app.config['DEBUG'] = os.getenv("LICSE_DEBUG")
    app.config['ENV'] = os.getenv("LICSE_ENV")
    app.config["SECRET_KEY"] = os.getenv('LICSE_COOKIE_SECRETKEY')
    api.init_app(app)

    api.add_namespace(licse_status_ns)
    api.add_namespace(licse_auth_ns)
    api.add_namespace(licse_db_ns)
    api.add_namespace(licse_chat_ns)
    api.add_namespace(licse_root_ns)

    return app
