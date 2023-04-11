#!/usr/bin/env python3
"""11-students"""


def top_students(mongo_collection):
    """function that returns all students sorted by average score:"""
    students_avg = mongo_collection.aggregrate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"avarageScore": -1}}
    ])

    return students_avg
