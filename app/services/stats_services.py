from fastapi import Request
from dotenv import dotenv_values

from . import keycloak_services


config = dotenv_values(".env")

def get_stats(request: Request):
    try:
        # Read uvicorn_log.txt file and count the number of lines
        with open("uvicorn_log.txt", "r") as f:
            lines = f.readlines()
            num_queries = len(lines)
        logs = True
    except FileNotFoundError:
        num_queries = "Unknown"
        logs = False
    try:
        num_users = len(keycloak_services.get_all_users())
        keycloak = True
    except Exception:
        num_users = "Unknown"
        keycloak = False
    try:
        record_one_count = request.app.database[
            config["RECORD_ONE_NAME"]].count_documents({})
        mongoDB = True
    except Exception:
        record_one_count = "Unknown"
        mongoDB = False
    try:
        record_two_count = request.app.database[
            config["RECORD_TWO_NAME"]].count_documents({})
    except Exception:
        record_two_count = "Unknown"
    stats = {
        "logs": logs,
        "keycloak": keycloak,
        "mongoDB": mongoDB,
        "queries": num_queries,
        "users": num_users,
        config["RECORD_ONE_NAME"]: record_one_count,
        config["RECORD_TWO_NAME"]: record_two_count,
    }
    return stats