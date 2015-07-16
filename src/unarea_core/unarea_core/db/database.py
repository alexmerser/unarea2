from flask_mongoengine import MongoEngine

__all__ = ['mongodb', 'Document', 'DynamicDocument']

mongodb = MongoEngine()
Document = mongodb.Document
DynamicDocument = mongodb.DynamicDocument
