from flask_security import Security


class UnareaSecurity(Security):
    def __new__(cls, app, datastore, *args, **kwargs):
        app.security = Security(app, datastore)
