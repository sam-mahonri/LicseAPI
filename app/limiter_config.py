from flask_limiter.util import get_remote_address

LIMITER_ENABLED = True
LIMITER_STORAGE_URI = "memory://"
LIMITER_KEY_FUNC = get_remote_address