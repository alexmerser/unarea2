from bson.objectid import ObjectId
from unarea_core.mongodb.bins import MONGODB
from unarea_core.mongodb.mongo import MongoCollection

__all__ = ["BaseIndexedDocument", "BaseDocument", "ObjectId"]


class BaseDocument(object):
    collection_name = None
    database = MONGODB
    structure = None
    shortcuts = None
    required = None
    associate_object = None

    def __init__(self):
        self._validate()
        self.collection = MongoCollection(self.database,
                                          self.collection_name,
                                          self.structure,
                                          self.shortcuts,
                                          self.required)
        super(BaseDocument, self).__init__()

    @classmethod
    def _validate(cls):
        assert cls.collection_name is not None, u"collection_name of %s can not be None" % cls.__name__
        assert cls.database is not None, u"database of %s can not be None" % cls.__name__
        assert cls.structure is not None, u"structure of %s must have at least one field" % cls.__name__
        if cls.required:
            for field in cls.required:
                assert field in cls.structure.iterkeys(), u"Required field %s must be in %s" % (field, cls.__name__)

    def get_by_id(self, document_id, to_object=False):
        """
        Get document from collection by id

        :param document_id: id of document
        :type document_id: ObjectId, str

        :param to_object: flag indicates is result will bi translated to domain specific object
        :type to_object: bool

        :return: document retrieved from db (dict) or None
        :rtype: dict | associated object

        :raises bson.errors.InvalidId - if invalid document_id was given as basestring and incorrect.
        """
        if isinstance(document_id, basestring):
            document_id = ObjectId(document_id)
        doc = self.collection.find_one({"_id": document_id})

        if to_object:
            assert self.associate_object is not None, u"No associated object specified for document %s" % self.__class__
            unpacked = {k: v for k, v in doc.iteritems() if not k.startswith(u"_")}
            return self.associate_object(**unpacked)
        return self.collection.find_one({"_id": document_id})


class BaseIndexedDocument(BaseDocument):
    indexed_fields = []

    def __init__(self):
        super(BaseIndexedDocument).__init__()
        assert len(self.indexed_fields) > 0, u"indexed_fields must contain at least one field"
        for field in self.indexed_fields:
            assert field in self.structure, u"%s must present in %ss structure" % (field, self.__class__)
        self.collection.ensure_index(self.indexed_fields)
