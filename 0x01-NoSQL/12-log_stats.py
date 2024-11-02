#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def print_nginx_logs_stats(nginx_collection):
    """
    Display stats about Nginx logs in MongoDB
    """
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = len(list(nginx_collection.find({"method": method.upper()})))
        print(f"    method {method}: {count}")

    status_check = len(list(nginx_collection.find(
        {"method": "GET", "path": "/status"}
    )))
    print(f"{status_check} status check")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_logs_stats(nginx_collection)

