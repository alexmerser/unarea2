# -*- coding: utf-8 -*-
from flask import Flask

from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware


def create_app(package_name, settings_override=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the platform.

    :param package_name: application package name
    :param settings_override: a dictionary of settings to override

    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('unarea_server.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    register_blueprints(app, app.config['MOD_PATH'])

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app
