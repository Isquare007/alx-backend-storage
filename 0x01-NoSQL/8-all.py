#!/usr/bin/env python3
"""lists all the documents in a mongo db collection"""


def list_all(mongo_collection):
    """list all documents"""
    if mongo_collection.find().count() == 0:
        return []
    return mongo_collection.find()
