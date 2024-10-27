#!/usr/bin/env python3
""" 8-all """


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection."""
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
