import csv
from fastapi import APIRouter, Depends, Body, Response, HTTPException, \
    Request, Query, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from dotenv import dotenv_values
from ..models.user_model import User
from ..models.record_one_model import RecordOne, NewRecordOne, \
    UpdateRecordOne, UpdateRecordOneConnections, UpdateRecordOneContent
from ..services import keycloak_services, record_one_services, \
    record_two_services, plot_services


router = APIRouter()


#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


@router.get("",
    responses={
        200: {
            "model": List[RecordOne],
            "description": f"List of all {config['RECORD_ONE_TAG']}."
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_ONE_TAG']}."
        }
    },
    summary=f"Retrieve a list of all {config['RECORD_ONE_TAG']}."
)
def get_records_one(
    response: Response, request: Request,
    title: str = Query(
        None, description="Optional - String to search in the title"
    ),
    current_user: User = Depends(keycloak_services.optional_get_current_user)
):
    response.status_code = 200
    if current_user:
        username = current_user['username']
    else:
        username = None
    return record_one_services.get_records_one(username, title, request)


@router.get("/me",
    responses={
        200: {
            "model": List[RecordOne],
            "description": f"List of {config['RECORD_ONE_TAG']} " + \
                "belonging to the current user."
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_ONE_TAG']}."
        }
    },
    summary=f"Retrieve a list of {config['RECORD_ONE_TAG']} " + \
        "belonging to the current user."
)
def get_records_one_me(
    response: Response, request: Request,
    title: str = Query(
        None, description="Optional - String to search in the title"
    ),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    response.status_code = 200
    return record_one_services.get_records_one_me(
        current_user['username'], title, request
    )


@router.get("/{id}",
    responses={
        200: {
            "model": RecordOne,
            "description": f"The {config['RECORD_ONE_NAME']}"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_ONE_NAME']}"
        }
    },
    summary=f"Retrieve a {config['RECORD_ONE_NAME']} given its ID."
)
def get_record_one(
    response: Response, request: Request, id: str
):
    record = record_one_services.get_record_one(id, request)
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )


# Make a route that given the id of the record and the x and y axis, it returns a plot of the content
@router.get("/{id}/plot/{x}/{y}",
    responses={
        200: {
            "description": f"The plot of the {config['RECORD_ONE_NAME']}"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error retrieving the " + \
                f"{config['RECORD_ONE_NAME']}"
        }
    },
    summary=f"Retrieve a plot of a {config['RECORD_ONE_NAME']} given its ID."
)
def get_record_one_plot(
    request: Request, id: str, x: str, y: str
):
    record = record_one_services.get_record_one(id, request)
    if record:
        return HTMLResponse(
            content=plot_services.plot(record, x, y),
            status_code=200
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )


@router.post("", 
    responses={
        201: {
            "model": RecordOne,
            "description": f"{config['RECORD_ONE_NAME']} successfully created"
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
            "description": f"Error creating the {config['RECORD_ONE_NAME']}"
        }
    },
    summary=f"Create a new {config['RECORD_ONE_NAME']}."
)
def create_record_one(
    response: Response, request: Request, record_one: NewRecordOne = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    new_record_one = jsonable_encoder(record_one)
    # Check if title is unique
    unique = record_one_services.title_is_unique(
        new_record_one["title"], request
    )
    if unique:
        # Check if the editors or viewers are valid users
        if "editors" in new_record_one and new_record_one["editors"]:
            for editor in new_record_one["editors"]:
                if not keycloak_services.user_exists(editor):
                    raise HTTPException(
                        status_code=404,
                        detail='Editor not found'
                    )
        if "viewers" in new_record_one and new_record_one["viewers"]:
            for viewer in new_record_one["viewers"]:
                if not keycloak_services.user_exists(viewer):
                    raise HTTPException(
                        status_code=404,
                        detail='Viewer not found'
                    )
        # Check if the connections are valid
        if "connections" in new_record_one and new_record_one["connections"]:
            for connection in new_record_one["connections"]:
                record_type = connection["type"]
                record_id = connection["id"]
                if record_type == config['RECORD_TWO_NAME']:
                    # Check if the record exists
                    record_two = record_two_services.get_record_two(
                        record_id, request
                    )
                    if not record_two:
                        raise HTTPException(
                            status_code=404,
                            detail=f'{config["RECORD_TWO_NAME"]} not found'
                        )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail='Connection type not found'
                    )

        # Create the record
        response.status_code = 201
        new_record = record_one_services.create_record_one(
            new_record_one, current_user['username'], request
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


@router.put("/{id}",
    responses={
        200: {
            "model": RecordOne,
            "description": f"The {config['RECORD_ONE_NAME']} has been" + \
                " updated successfully"
        },
        400: {
            "description": "Invalid request body"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        }
    },
    summary=f"Update a {config['RECORD_ONE_NAME']} given its ID."
)
def update_record_one(
    response: Response, request: Request, id: str,
    record_one: UpdateRecordOne = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    record_one = jsonable_encoder(record_one)
    # Check if the record exists
    record = record_one_services.get_record_one(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )
    # Check if the record is owned or editable by the current user
    editable = record_one_services.is_editable(
        id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        )
    record = record_one_services.update_record_one(
        id, record_one, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        )


@router.put("/{id}/connections",
    responses={
        200: {
            "model": RecordOne,
            "description": f"The {config['RECORD_ONE_NAME']} has been" + \
                " updated successfully"
        },
        400: {
            "description": "Invalid request body"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        }
    },
    summary=f"Update the connections of a {config['RECORD_ONE_NAME']} " + \
        "given its ID."
)
def update_record_one_connections(
    response: Response, request: Request, id: str,
    record_one_connections: UpdateRecordOneConnections = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    record_one_connections = jsonable_encoder(record_one_connections)
    # Check if the record exists
    record = record_one_services.get_record_one(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )
    # Check if the record is owned or editable by the current user
    editable = record_one_services.is_editable(
        id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        )
    record = record_one_services.update_record_one_connections(
        id, record_one_connections, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        )


@router.put("/{id}/content",
    responses={
        200: {
            "model": RecordOne,
            "description": f"The {config['RECORD_ONE_NAME']} has been" + \
                " updated successfully"
        },
        400: {
            "description": "Invalid request body"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        }
    },
    summary=f"Update the content of a {config['RECORD_ONE_NAME']} " + \
        "given its ID."
)
def update_record_one_content(
    response: Response, request: Request, id: str,
    record_one_content: UpdateRecordOneContent = Body(),
    current_user: User = Depends(keycloak_services.get_current_user)
):
    record_one_content = jsonable_encoder(record_one_content)
    # Check if the record exists
    record = record_one_services.get_record_one(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )
    # Check if the record is owned or editable by the current user
    editable = record_one_services.is_editable(
        id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        )
    record = record_one_services.update_record_one_content(
        id, record_one_content, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        )


@router.put("/{id}/content/csv",
    responses={
        200: {
            "model": RecordOne,
            "description": f"The {config['RECORD_ONE_NAME']} has been" + \
                " updated successfully"
        },
        400: {
            "description": "Invalid request body"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        }
    },
    summary=f"Update the content of a {config['RECORD_ONE_NAME']} " + \
        "given its ID."
)
def update_record_one_content_csv(
    response: Response, request: Request, id: str, file: UploadFile,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    def csv_to_dict(file):
        """Convert a CSV file to a dictionary"""
        # Read the CSV file
        csv_file = file.read().decode('utf-8').splitlines()
        # Create a dictionary from the CSV file
        csv_dict = csv.DictReader(csv_file)
        # Convert the CSV file to a dictionary
        csv_dict = [row for row in csv_dict]
        return csv_dict

    # Read CSV from file and convert to dict
    vsc_content = csv_to_dict(file.file)
    # Check if the record exists
    record = record_one_services.get_record_one(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )
    # Check if the record is owned or editable by the current user
    editable = record_one_services.is_editable(
        id, current_user['username'], request)
    if not editable:
        raise HTTPException(
            status_code=403,
            detail="Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you or you are not an editor"
        )
    record_one_content = {
        'content': vsc_content,
        'operation': 'add'
    }
    record = record_one_services.update_record_one_content(
        id, record_one_content, request
    )
    if record:
        response.status_code = 200
        return record
    else:
        raise HTTPException(
            status_code=500,
            detail="There was an error updating the " + \
                f"{config['RECORD_ONE_NAME']}."
        )


@router.delete("/{id}",
    responses={
        204: {
            "description": f"{config['RECORD_ONE_NAME']} deleted"
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the {config['RECORD_ONE_NAME']}" + \
                " does not belong to you"
        },
        404: {
            "description": f"{config['RECORD_ONE_NAME']} not found"
        },
        500: {
            "description": "There was an error deleting the " + \
                f"{config['RECORD_ONE_NAME']}"
        }
    },
    summary=f"Delete a {config['RECORD_ONE_NAME']} given its ID."
)
def delete_record_one(
    response: Response, request: Request, id: str,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    # Check if the record exists
    record = record_one_services.get_record_one(id, request)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"{config['RECORD_ONE_NAME']} not found"
        )
    # Check if the record is owned by the current user
    editable = record_one_services.is_owned(
        id, current_user['username'], request
    )
    if not editable:
        raise HTTPException(
            status_code=403,
            detail='Record not owned by you'
        )
    deleted = record_one_services.delete_record_one(
        id, request
    )
    if deleted:
        response.status_code = 204
        return ''
    else:
        raise HTTPException(
            status_code=500,
            detail=f"There was an error deleting the " + \
                f"{config['RECORD_ONE_NAME']}"
        )
