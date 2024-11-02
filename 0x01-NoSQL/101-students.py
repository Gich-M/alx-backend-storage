#!/usr/bin/env python3
"""
Module for MongoDB operations - Top students by average score
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    Args:
        mongo_collection: pymongo collection object
    Returns:
        list of students sorted by average score
    """
    return mongo_collection.aggregate([
        {
            "$addFields": {
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ])
