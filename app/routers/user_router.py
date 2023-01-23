from fastapi import APIRouter, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
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


@router.get("/me", responses={
        200: {
            "model": User,
            "description": "Info from the user"
        },
        404: {
            "description": "User not found",
        },
        500: {
            "description": "Error getting the user info"
        }
    }
)
async def read_users_me(
    current_user: User = Depends(keycloak_services.get_current_user)):
    return current_user


@router.delete("/{user_id}", responses={
        204: {
            "description": "User deleted"
        },
        403: {
            "description": "FORBIDDEN: You cannot delete the user",
        },
        500: {
            "description": "Error deleting the user"
        }
    }
)
def delete_user(
    response: Response, user_id: str,
    current_user: User = Depends(keycloak_services.get_current_user)
):
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
        403: {
            "description": "FORBIDDEN: You cannot modify the user",
        },
        500: {
            "description": "Error occurred while modifying the user"
        }
    }, summary="Update user info. NOTE: The updated info will be shown " + \
        "when you refresh the token"
)
def update_user(
    user_id: str, update_info: UpdateUser, response: Response,
    current_user: User = Depends(keycloak_services.get_current_user),
):
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
