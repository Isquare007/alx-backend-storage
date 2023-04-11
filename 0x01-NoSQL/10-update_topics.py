#!/usr/bin/env python3
"""Python function that changes all topics of a
school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """changes topic"""
    query = {"name": name}
    topic_val = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, topic_val)
