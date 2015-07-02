from bson import ObjectId
from pymongo import MongoClient
from unarea_core.mongodb.exceptions import InvalidKeyValueError, DuplicateKeyError, UnexpectedKeyError

__all__ = ["MongoDBObject", "MongoCollection"]


class MongoDBObject(object):
    def __init__(self, name, host, port=27017):
        """
        Mongodb specification object

        :param name: database name
        :type name: str

        :param host: database host
        :type host: str

        :param port: database port
        :type port: int
        """
        self.name = name
        self.host = host
        self.port = port


class MongoCollection(object):
    connections = {}

    def __init__(self, database, collection_name, structure, shortcuts, required=None):

        """
        :param database:
        :type database: MongoDBObject

        :param collection_name:
        :type collection_name: unicode

        :param structure:
        :type structure: dict

        :param shortcuts:
        :type shortcuts: dict

        :param required:
        :type required: Iterable | None
        """
        self._structure = structure
        self._shortcuts = shortcuts
        self.required = required

        sc = self._shortcuts.values()
        if len(sc) != len(set(sc)):
            raise ValueError(u"Duplicates values in shortcuts %r")

        self._back_shortcuts = {value: key for key, value in self._shortcuts.iteritems()}
        self._collection_spec = collection_name

        self._database = database
        self._collection_name = collection_name

        self._collection = None

    @property
    def collection(self):
        if self._collection is None:
            if self._database.name not in MongoCollection.connections:
                host = self._database.host
                port = self._database.port
                db_name = self._database.name
                MongoCollection.connections[self._database.name] = MongoClient(host=host, port=port)[db_name]
            db = MongoCollection.connections[self._database.name]
            self._collection = db[self._collection_name]
        return self._collection

    def validate_structure(self, values_dict):
        for key, value in values_dict.items():
            if key in self._structure:
                if not isinstance(value, self._structure[key]) and value is not None:
                    raise InvalidKeyValueError(key, value, self._structure[key])
            else:
                raise UnexpectedKeyError(key, u'structure dictionary')

    def translate_to_shortcuts(self, values_dict):
        res = {}
        for key, value in values_dict.items():
            new_key = self._shortcuts[key] if not key.startswith("$") else key
            res[new_key] = value if not isinstance(value, dict) else self.translate_to_shortcuts(value)

        return res

    def untranslate_shortcuts(self, short_dict):
        res = {}
        for key, value in short_dict.iteritems():
            new_key = self._back_shortcuts[key]
            res[new_key] = value if not isinstance(value, dict) else self.untranslate_shortcuts(value)

        return res

    def translate_field(self, field_name):
        if field_name.startswith(u"$"):
            return u"$" + self._shortcuts[field_name[1:]]
        else:
            return self._shortcuts[field_name]

    def update_many(self, insert_objects, update_query, update_fields):
        try:
            self.collection.insert(insert_objects, continue_on_error=True, w=1)
        except DuplicateKeyError:
            self.collection.update(update_query, {u'$set': update_fields}, multi=True)

    def insert(self, doc_or_docs, ignore_duplicates=False):
        try:
            return self.collection.insert(doc_or_docs, continue_on_error=ignore_duplicates, w=1)
        except DuplicateKeyError:
            if not ignore_duplicates:
                raise

    def find_one(self, query, sort=None):
        return self.collection.find_one(query, sort=sort)

    def find(self, query, limit=0, sort=None):
        return self.collection.find(query, limit=limit, sort=sort)

    def remove(self, query):
        self.collection.remove(query, w=1)

    def update(self, spec, document, multi=False):
        return self.collection.update(spec, document, multi=multi, w=1)

    def ensure_index(self, keys):
        return self.collection.ensure_index(keys)