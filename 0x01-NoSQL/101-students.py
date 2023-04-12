#!/usr/bin/env python3
"""11-students"""


def top_students(mongo_collection):
    """function that returns all students sorted by average score:"""
    pipeline = [
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    top_student = mongo_collection.aggregate(pipeline)
    return list(top_student)
