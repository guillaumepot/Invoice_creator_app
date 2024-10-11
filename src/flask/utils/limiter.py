#flask/services/limiter.py


# Lib
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app



# Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,   
    default_limits=["1000 per hour"]  
)