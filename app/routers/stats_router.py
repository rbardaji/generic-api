from fastapi import APIRouter, Request
from dotenv import dotenv_values
from ..services import stats_services

router = APIRouter()

#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


@router.get("",
    summary="Retrieve the stats of the API.")
def get_stats(request: Request):
    return stats_services.get_stats(request)
