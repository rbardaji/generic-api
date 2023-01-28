from fastapi import APIRouter, Depends, Body, Response, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from typing import List
from dotenv import dotenv_values
from ..models.user_model import User
from ..models.record_two_model import RecordTwo, NewRecordTwo, UpdateRecordTwo
from ..services import keycloak_services, record_two_services

router = APIRouter()


#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


@router.get("",
    responses={
        200: {
            "model": List[RecordTwo],
            "description": f"List of all {config['RECORD_TWO_TAG']}."
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_TWO_TAG']}."
        }
    },
    summary=f"Retrieve a list of all {config['RECORD_TWO_TAG']}."
)
def get_records_two(
    response: Response, request: Request,
    current_user: User = Depends(keycloak_services.optional_get_current_user)
):
    response.status_code = 200
    if current_user:
        username = current_user['username']
    else:
        username = None
    return record_two_services.get_records_two(username, request)


@router.get("/me",
    responses={
        200: {
            "model": List[RecordTwo],
            "description": f"List of {config['RECORD_TWO_TAG']} " + \
                "belonging to the current user."
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_TWO_TAG']}."
        }
    },
    summary=f"Retrieve a list of {config['RECORD_TWO_TAG']} " + \
        "belonging to the current user."
)
def get_records_one_me(
    response: Response, request: Request,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    response.status_code = 200
    return record_two_services.get_records_two_me(
        current_user['username'], request
    )


@router.post("", 
    responses={
        201: {
            "model": RecordTwo,
            "description": f"{config['RECORD_TWO_NAME']} successfully created"
        },
        400: {
            "description": "Invalid request body"
        },
        404: {
            "description": "Editor or viewer not found"
        },
        409: {
                "description": "Title already exists",
        },
        500: {
            "description": f"Error creating the {config['RECORD_TWO_NAME']}"
        }
    },
    summary=f"Create a new {config['RECORD_TWO_NAME']}."
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


@router.get("/{id}",
    responses={
        200: {
            "model": RecordTwo,
            "description": f"The {config['RECORD_TWO_NAME']}"
        },
        404: {
            "description": f"{config['RECORD_TWO_NAME']} not found"
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_TWO_NAME']}."
        }
    },
    summary=f"Retrieve a {config['RECORD_TWO_NAME']} given its ID."
)
def get_record_two(
    response: Response, request: Request, id: str
):
    record = record_two_services.get_record_two(id, request)
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )


@router.put("/{id}",
    responses={
        200: {
            "model": RecordTwo,
            "description": f"The {config['RECORD_TWO_NAME']} has been" + \
                " updated successfully"
        },
        400: {
            "description": "Invalid request body"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_TWO_NAME']}" + \
                " does not belong to you or you are not an editor"
        },
        404: {
            "description": f"{config['RECORD_TWO_NAME']} not found"
        },
        500: {
            "description": "There was an error updating the " + \
                f"{config['RECORD_TWO_NAME']}"
        }
    },
    summary=f"Update a {config['RECORD_TWO_NAME']} given its ID."
)
def update_record_two(
    response: Response, request: Request, id: str,
    record_two: UpdateRecordTwo = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    record_two = jsonable_encoder(record_two)
    # Check if the record exists
    record = record_two_services.get_record_two(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_TWO_NAME']} not found"
        )
    # Check if the record is owned or editable by the current user
    editable = record_two_services.is_editable(
        id, current_user['username'], request
    )
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_TWO_NAME']}" + \
                " does not belong to you or you are not an editor"
        )
    record = record_two_services.update_record_two(
        id, record_two, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error updating the " + \
                f"{config['RECORD_TWO_NAME']}"
        )


@router.delete("/{id}",
    responses={
        204: {
            "description": f"{config['RECORD_TWO_NAME']} deleted"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_TWO_NAME']}" + \
                " does not belong to you"
        },
        404: {
            "description": f"{config['RECORD_TWO_NAME']} not found"
        },
        500: {
            "description": "There was an error deleting the " + \
                f"{config['RECORD_TWO_NAME']}"
        }
    },
    summary=f"Delete a {config['RECORD_TWO_NAME']} given its ID."
)
def delete_record_two(
    response: Response, request: Request, id: str,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    # Check if the record exists
    record = record_two_services.get_record_two(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_TWO_NAME']} not found"
        )
    # Check if the record is owned by the current user
    editable = record_two_services.is_owned(
        id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_TWO_NAME']}" + \
                " does not belong to you"
        )
    deleted = record_two_services.delete_record_two(
        id, request
    )
    if deleted:
        response.status_code = 204
        return ''
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error deleting the " + \
                f"{config['RECORD_TWO_NAME']}"
        )
