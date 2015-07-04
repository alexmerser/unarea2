# -*- coding: utf-8 -*-
"""
    overholt.helpers
    ~~~~~~~~~~~~~~~~

    overholt helpers module
"""

import pkgutil
import os
import imp

from flask.json import JSONEncoder as BaseJSONEncoder


def register_blueprints(app, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_path: the package path
    """
    mod_path = package_path
    dir_list = os.listdir(mod_path)
    mods = {}

    for module in dir_list:
        if os.path.isdir(os.path.join(mod_path, module)) and os.path.exists(
                os.path.join(mod_path, module, '__init__.py')):
            f, filename, description = imp.find_module(module, [mod_path])
            mods[module] = imp.load_module(module, f, filename, description)
            blueprint = getattr(mods[module], 'module')
            if blueprint.name not in app.blueprints:
                app.register_blueprint(blueprint)
            else:
                app.logger.error("CONFLICT:{0} already registered.".format(
                    filename))

        # This part of code load blueprint from python module (for more flexibility to extend base system)
        elif pkgutil.os.path.isfile(pkgutil.os.path.join(mod_path, module)):
            name, ext = os.path.splitext(module)
            if ext == '.py' and not name == '__init__':
                f, filename, description = imp.find_module(name, [mod_path])
                mods[module] = imp.load_module(name, f, filename, description)
                blueprint = getattr(mods[module], 'module')
                if blueprint.name not in app.blueprints:
                    app.register_blueprint(blueprint)
                else:
                    app.logger.error("CONFLICT:{0} already registered.".format(
                        filename))


class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        if isinstance(obj, JsonSerialized):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerialized(object):
    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv
