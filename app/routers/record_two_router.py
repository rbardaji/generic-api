from fastapi import APIRouter, Depends, Body, Response, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models.user_model import User
from ..models.record_two_model import RecordTwo, NewRecordTwo, UpdateRecordTwo
from ..services import keycloak_services, record_two_services

router = APIRouter()


@router.get("",
    responses={
        200: {
            "model": List[RecordTwo],
            "description": "List of records"
        },
        500: {
            "description": "Error getting the records"
        }
    }
)
def get_records_one(
    response: Response, request: Request,
    current_user: User = Depends(keycloak_services.optional_get_current_user)
):
    response.status_code = 200
    if current_user:
        username = current_user['username']
    else:
        username = None
    return record_two_services.get_records_one(username, request)


@router.get("/me",
    responses={
        200: {
            "model": List[RecordTwo],
            "description": "List of records"
        },
        500: {
            "description": "Error getting the records"
        }
        }
)
def get_records_one_me(
    response: Response, request: Request,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    response.status_code = 200
    return record_two_services.get_records_one_me(
        current_user['username'], request
    )

@router.post("", 
    responses={
        201: {
            "model": User,
            "description": "New record created"
        },
        409: {
                "description": "Title already exists",
        },
        500: {
            "description": "Error creating the record"
        }
    }
)
def create_record_two(
    response: Response, request: Request, record_two: NewRecordTwo = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    new_record_two = jsonable_encoder(record_two)
    # Check if title is unique
    unique = record_two_services.title_is_unique(
        new_record_two["title"], request
    )
    if unique:
        # Check if the editors or viewers are valid users
        if "editors" in new_record_two and new_record_two["editors"]:
            for editor in new_record_two["editors"]:
                if not keycloak_services.user_exists(editor):
                    raise HTTPException(
                        status_code=404,
                        detail='Editor not found'
                    )
        if "viewers" in new_record_two and new_record_two["viewers"]:
            for viewer in new_record_two["viewers"]:
                if not keycloak_services.user_exists(viewer):
                    raise HTTPException(
                        status_code=404,
                        detail='Viewer not found'
                    )
        response.status_code = 201
        new_record = record_two_services.create_record_two(
            new_record_two, current_user['username'], request
        )
        # Convert the _id field to id
        new_record["id"] = str(new_record["_id"])
        del new_record["_id"]
        return new_record

    else:
        raise HTTPException(
            status_code=409,
            detail='Title already exists'
        )


@router.get("/{record_id}",
    responses={
        200: {
            "model": RecordTwo,
            "description": "The record"
        },
        404: {
            "description": "Record not found"
        },
        500: {
            "description": "Error getting the record"
        }
    }
)
def get_record_two(
    response: Response, request: Request, record_id: str
):
    record = record_two_services.get_record_two(record_id, request)
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=404,
            detail='Record not found'
        )


@router.put("/{record_id}",
    responses={
        200: {
            "model": RecordTwo,
            "description": "The updated record"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Record not found"
        },
        500: {
            "description": "Error updating the record"
        }
    }
)
def update_record_two(
    response: Response, request: Request, record_id: str,
    record_two: UpdateRecordTwo = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    record_two = jsonable_encoder(record_two)
    # Check if the record exists
    record = record_two_services.get_record_two(record_id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail='Record not found'
        )
    # Check if the record is owned or editable by the current user
    editable = record_two_services.is_editable(
        record_id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail='Record not editable by you'
        )
    record = record_two_services.update_record_two(
        record_id, record_two, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=404,
            detail='Record not found'
        )


@router.delete("/{record_id}",
    responses={
        204: {
            "description": "Record deleted"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Record not found"
        },
        500: {
            "description": "Error deleting the record"
        }
    }
)
def delete_record_two(
    response: Response, request: Request, record_id: str,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    # Check if the record exists
    record = record_two_services.get_record_two(record_id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail='Record not found'
        )
    # Check if the record is owned by the current user
    editable = record_two_services.is_owned(
        record_id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail='Record not owned by you'
        )
    deleted = record_two_services.delete_record_two(
        record_id, request
    )
    if deleted:
        response.status_code = 204
        return ''
    else:
        raise HTTPException(
            status_code=404,
            detail='Record not found'
        )

