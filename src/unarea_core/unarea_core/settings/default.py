from unarea_core.settings import get_config_file


class DefaultSettings(object):
    DEBUG = True


config = {
    "default": "unarea_core.settings.default.DefaultSettings"
}


def configure_app(app):
    filename = get_config_file()
    app.config.from_pyfile(filename, silent=True)
