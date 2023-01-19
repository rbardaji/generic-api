from fastapi import APIRouter, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..models.user_model import NewUser, User
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
            "description": "Error creating the user"
        }
    }
)
async def create_user(new_user: NewUser, response: Response):
    # Decode the new user data
    user = jsonable_encoder(new_user)

    # Create the new user in the keycloak server
    status_code = keycloak_services.create_user_keycloak(
        username=user['username'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=user['password']
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
            detail='Error creating the user'
        )
