from bson import ObjectId
from unarea_core.mongodb.exceptions import InvalidKeyValueError
from unarea_core.mongodb.documents import BaseDocument
from unarea_core.mongodb.mongo import MongoDBObject
from unittest import TestCase

TEST_DB = MongoDBObject('unarea_test', 'localhost', 27017)

class TestObject(object):
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def as_dict(self):
        return {
            u'field1': self.field1,
            u'field2': self.field2
        }


class TestDoc(BaseDocument):
        collection_name = u'mongo_testing'
        database = TEST_DB
        structure = {
            u'field1': unicode,
            u'field2': int
        }

        shortcuts = {
            u'field1': u'f1',
            u'field2': u'f2'
        }


class BaseDocumentSpec(TestCase):

    def setUp(self):
        self.to = TestObject(u'uniq', 234)
        self.ts = TestDoc()
        self.ids_to_del = []

        self._rid = self.ts.collection.insert(self.to.as_dict())

    def tearDown(self):
        if self.ids_to_del:
            self.ts.collection.remove({"_id": {"$in": self.ids_to_del}})

        self.ts.collection.remove({"_id": self._rid})

    def test_validation_success_field(self):
        self.ts.collection.validate_structure(self.to.as_dict())

    def test_validation_failed_field(self):
        fto = TestObject(123, '123')
        with self.assertRaises(InvalidKeyValueError):
            self.ts.collection.validate_structure(fto.as_dict())

    def test_translate_structure_to_shortcut(self):
        res = self.ts.collection.translate_to_shortcuts(self.to.as_dict())
        self.assertEqual({u'f1': u'uniq', u'f2': 234}, res)

    def test_untranslation_from_shortcuts(self):
        res = self.ts.collection.translate_to_shortcuts(self.to.as_dict())
        res2 = self.ts.collection.untranslate_shortcuts(res)
        self.assertEqual({u'field1': u'uniq', u'field2': 234}, res2)

    def test_insertion(self):
        res = self.ts.collection.insert(self.to.as_dict())
        self.assertIsNotNone(res)
        self.assertIsInstance(res, ObjectId)
        self.ids_to_del.append(res)

    def test_search(self):
        res = self.ts.collection.find({})
        self.assertIsNotNone(res)
        lres = [r for r in res]
        self.assertEqual(len(lres), 1)
