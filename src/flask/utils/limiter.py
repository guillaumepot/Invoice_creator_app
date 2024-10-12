#flask/services/limiter.py


# Lib
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.config import DEFAULT_LIMITER_LIMITS



# Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[DEFAULT_LIMITER_LIMITS]  
)

def init_limiter(app):
    limiter.init_app(app)
    return limiter