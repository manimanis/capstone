import os


from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from config import config

from .auth import init_auth, AuthError

db = SQLAlchemy()
oauth = None
auth0 = None
ENDPOINTS_BASE_URL = os.environ.get('ENDPOINTS_BASE_URL')


def create_app(config_name):
    global auth0, oauth, db
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    oauth, auth0 = init_auth(app)
    CORS(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .frontend import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({
            'success': False,
            'code': e.code,
            'name': e.name,
            'description': e.description
        }), e.code

    @app.errorhandler(AuthError)
    def handle_exception(e):
        return jsonify({
            'success': False,
            'code': e.status_code,
            'name': e.error,
            'description': e.error
        }), e.code

    return app
