#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def print_nginx_logs_stats():
    """
    Display stats about Nginx logs in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')

    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method.upper()})
        print(f"    method {method}: {count}")

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")

    print("IPs:")
    ip_pipeline = [
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    ip_logs = nginx_collection.aggregate(ip_pipeline)

    for ip in ip_logs:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    print_nginx_logs_stats()
