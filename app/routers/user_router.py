import yaml

from fastapi import APIRouter, Response, HTTPException, status, Depends, \
    UploadFile
from fastapi.encoders import jsonable_encoder
from typing import List

from ..models.user_model import NewUser, User, UpdateUser
from ..services import keycloak_services

router = APIRouter()


# Define a route for the post a new user
@router.post('',
    responses={
        201: {
            "model": User,
            "description": "New user created"
        },
        409: {
                "description": "Username or email already exists",
        },
        500: {
            "description": "There was an error creating the new user"
        }
    },
    summary="Create a new user."
)
async def create_user(new_user: NewUser, response: Response):
    # Decode the new user data
    user = jsonable_encoder(new_user)

    # Create the new user in the keycloak server
    try:
        status_code = keycloak_services.create_user_keycloak(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=user['password']
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error connectiong with the AAI'
        )
    if status_code == 201:
        # Get info from user
        user_info = keycloak_services.get_user_info(user['username'])
        response.status_code = 201
        return user_info
    elif status_code == 409:
        raise HTTPException(
            status_code=409,
            detail='Username or email already exists'
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error creating the new user'
        )


# Define a route that creates a new user with a yanl file
@router.post('/yaml',
    responses={
        201: {
            "model": User,
            "description": "New user created"
        },
        409: {
                "description": "Username or email already exists",
        },
        500: {
            "description": "There was an error creating the new user"
        }
    },
    summary="Create a new user using a YAML file."
)
async def create_user_yaml(response: Response, file: UploadFile,):
     # Decode the new user data
    file_content = file.file.read()
    user = yaml.safe_load(file_content)

    # Create the new user in the keycloak server
    try:
        status_code = keycloak_services.create_user_keycloak(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=user['password']
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error connectiong with the AAI'
        )
    if status_code == 201:
        # Get info from user
        user_info = keycloak_services.get_user_info(user['username'])
        response.status_code = 201
        return user_info
    elif status_code == 409:
        raise HTTPException(
            status_code=409,
            detail='Username or email already exists'
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error creating the new user'
        )



@router.get("/me", responses={
        200: {
            "model": User,
            "description": "Info from the user"
        },
        401: {
            "description": "Unauthorized - Could not validate credentials",
        },
        500: {
            "description": "There was an error getting the user information"
        }
    },
    summary="Retrieve the information from the current user."
)
async def read_users_me(
    current_user: User = Depends(keycloak_services.get_current_user)):
    return current_user


@router.delete("/{user_id}", responses={
        204: {
            "description": "User deleted"
        },
        401: {
            "description": "Unauthorized - Could not validate credentials",
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the user ID does not belong to you",
        },
        500: {
            "description": "There was an error deleting the user"
        }
    },
    summary="Delete a user. NOTE: You only can delete yourself."
)
async def delete_user(
    response: Response, user_id: str,
    current_user: User = Depends(keycloak_services.get_current_user)
):
    # Check if the current user is the test user
    if current_user['id'] == 'test':
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error connectiong with the AAI'
        )

    # Check if the user is trying to delete itself
    if user_id != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You cannot delete the user with id {user_id}"
        )
    # Delete the user from the Keycloak server
    status_code = keycloak_services.delete_user_keycloak(current_user['id'])
    if status_code == 204:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting the user"
        )


@router.put(
    "/{user_id}", responses={
        204: {
            "description": "User info updated"
        },
        401: {
            "description": "Unauthorized - Could not validate credentials",
        },
        403: {
            "description": "Forbidden - You are not authorized to perform " + \
                f"this operation because the user ID does not belong to you",
        },
        500: {
            "description": "There was an error updating the user"
        }
    },
    summary="Update user info. NOTE: The updated info will be shown " + \
        "when you refresh the token"
)
async def update_user(
    user_id: str, update_info: UpdateUser, response: Response,
    current_user: User = Depends(keycloak_services.get_current_user),
):
    # Check if the current user is the test user
    if current_user['id'] == 'test':
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error connectiong with the AAI'
        )

    # Check if the user is trying to delete itself
    if user_id != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You cannot modify the user with id {user_id}"
        )

    # Decode the JSON body
    info_encoded = jsonable_encoder(update_info)
    response_code = keycloak_services.update_user(
        user_id=current_user['id'], new_user_information=info_encoded
    )
    if response_code != 204:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while modifying the user"
        )
    else:
        response.status_code = 204
        return response


@router.get('',
    responses={
        200: {
            "model": List[User],
            "description": "List of users",
        },
        401: {
            "description": "Unauthorized - Could not validate credentials",
        },
        500: {
            "description": "There was an error retrieving the users"
        }
    },
    summary="Retrieve all users."
)
async def read_users(
    _: User = Depends(keycloak_services.get_current_user)):
    # Get all users from the keycloak server
    try:
        users = keycloak_services.get_all_users()
        if 'error' in users:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Error getting the users'
            )
        return users
    except Exception:
        # Check if the current user is the test user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error connectiong with the AAI'
        )
