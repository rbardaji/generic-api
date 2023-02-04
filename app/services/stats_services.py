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
    except FileNotFoundError:
        num_queries = "Unknown"
    stats = {
        "queries": num_queries,
        "users": len(keycloak_services.get_all_users()),
        config["RECORD_ONE_NAME"]: request.app.database[
            config["RECORD_ONE_NAME"]
        ].count_documents({}),
        config["RECORD_TWO_NAME"]: request.app.database[
            config["RECORD_TWO_NAME"]
        ].count_documents({})
    }
    return stats