from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token_model import Token
from ..services import keycloak_services

router = APIRouter()

@router.post("", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()):
    keycloak_token = keycloak_services.user_token_keycloak(
        form_data.username, form_data.password
    )

    if not keycloak_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": keycloak_token, "token_type": "bearer"}
