#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB

"""
from pymongo import MongoClient


def print_nginx_logs_stats(nginx_collection):
    """
    Prints stats about Nginx request logs.
    """
    print("{} logs".format(nginx_collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        log_count = len(list(nginx_collection.find({"method": method})))
        print("\tmethod {}: {}".format(method, log_count))
    status_check = len(list(
        nginx_collection.find({"method": "GET", "path": "/status"})
    ))
    print("{} status check".format(status_check))


def run():
    """Provides some stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient("mongodb://127.0.0.1:27017")
    print_nginx_logs_stats(client.logs.nginx)


if __name__ == "__main__":
    run()

