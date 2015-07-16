from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from unarea_core.ext.security import UnareaSecurity

from unarea_core.db import mongodb
from unarea_accounts.models import USER_MODEL


from unarea_core.settings.utils import load_env_config, load_app_config
from unarea_science.bins import SCIENCE
from unarea_accounts.bins import ACCOUNTS

def configure_extensions(app):
    mongodb.init_app(app)

    UnareaSecurity(app, USER_MODEL)

def create_app():
    """Create Flask app."""
    app = Flask(__name__)

    env_config = load_env_config()
    app.config.from_pyfile(env_config)
    app_config = load_app_config(app.config['UNAREA_ENV_TYPE'].lower())
    app.config.from_object(app_config)

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    configure_extensions(app)
    app.register_blueprint(ACCOUNTS)
    app.register_blueprint(SCIENCE)
    return app
