#!/usr/bin/env python3
"""Python function that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of topics"""
    doc = mongo_collection.find({"topic": topic})
    doc_list = [item for item in doc]
    return doc_list
