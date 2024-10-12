#flask/utils/config.py


# Lib
import os
from passlib.context import CryptContext


# Env VARS
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
DEBUG_MODE = os.getenv('FLASK_DEBUG', True)
DEFAULT_LIMITER_LIMITS = os.getenv('DEFAULT_LIMITER_LIMITS', "60 per minute")

CURRENT_VERSION = os.getenv('CURRENT_VERSION', 'v1')

FLASK_SECRET_APP_KEY = os.getenv("FLASK_SECRET_APP_KEY", "faf1Fz1daf8Z8z191Z")
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM', 'argon2')


MONGO_HOST= os.getenv('MONGO_HOST', 'invoice-mongodb')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_API_USERNAME = os.getenv('MONGO_API_USERNAME')
MONGO_API_PASSWORD = os.getenv('MONGO_API_PASSWORD')


# CryptContext
pwd_context = CryptContext(schemes=[HASH_ALGORITHM], deprecated="auto")

