# flask/app.py


# Lib
from flask import Flask, render_template, send_file, request, jsonify
from flask import session, redirect, url_for, flash, g
import io
import time
from uuid import uuid4


from routers.information import information_router
from routers.authentification import authentification_router
from routers.company import company_router
from utils.config import FLASK_HOST, FLASK_PORT, DEBUG_MODE, FLASK_SECRET_APP_KEY
from utils.limiter import init_limiter


# Flask
app = Flask(__name__)
app.secret_key = FLASK_SECRET_APP_KEY


"""
Limiter
"""
init_limiter(app)


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded"), 429
# Middleware to add processing time header
@app.before_request
def before_request():
    g.start_time = time.time()
@app.after_request
def after_request(response):
    process_time = time.time() - g.start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


"""
Routes & Routers
"""
@app.route('/')
def home():
    return jsonify({"message": "Hello World!"})
    #api_key = session.get('api_key')
    #return render_template('home.html', api_key=api_key)


app.register_blueprint(information_router, url_prefix='/info')
app.register_blueprint(authentification_router, url_prefix='/auth')
app.register_blueprint(company_router, url_prefix='/company')


# Start app
if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_MODE)