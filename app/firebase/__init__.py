
from app.db_config import get_config
import pyrebase

pb_set = get_config()
firebase = pyrebase.initialize_app(pb_set)

auth = firebase.auth()
db = firebase.database()

from . import auth
from . import db