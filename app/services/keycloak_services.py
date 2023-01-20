import json
import requests
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


# Client configuration
# keycloak_url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}'
# keycloak_openid = KeycloakOpenID(
#     server_url=keycloak_url,
#     client_id='admin-cli',
#     realm_name=config["KEYCLOAK_REALM"],
#     client_secret_key=config["KEYCLOAK_ADMIN_SECRET"],
#     verify=False
# )


def get_admin_header_keycloak():
    """
    This function is used to get the access token of the keycloak admin user
    """
    # header variable is used to specify the headers of the request
    header = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br"
    }
    # admin_user variable is used to specify the keycloak admin user credentials
    admin_user = {
        'username': config['KEYCLOAK_ADMIN'],
        'password': config['KEYCLOAK_ADMIN_PASSWORD'],
        'grant_type': 'password',
        'client_id': 'admin-cli',
        'client_secret': config['KEYCLOAK_ADMIN_SECRET']
    }

    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        '/realms/master/protocol/openid-connect/token'

    # tokens variable is used to store the access token
    tokens = json.loads(
        requests.post(
            url,
            data=admin_user,
            headers=header,
            verify=False
        ).content
    )

    #return the access token in the header
    return {
        "Content-Type": "application/json",
        'Authorization': 'Bearer ' + tokens['access_token'],
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br"
    }


def create_user_keycloak(username, first_name, last_name, email, password):
    """
    This function is used to create a new user in the keycloak server

    Parameters
    ----------
    username : str
        username of the new user
    first_name : str
        first name of the new user
    last_name : str
        last name of the new user
    email : str
        email of the new user
    password : str
        password of the new user

    Returns
    -------
    int
        status code of the request
    """
    #admin_header variable is used to store the access token of the keycloak admin user
    admin_header = get_admin_header_keycloak()
    #user variable is used to store the new user's details
    user = {
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'enabled': 'true',
        'username': username,
        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": False
            }
        ]
    }
    #url is used to create a new user in the keycloak server
    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/auth/admin/realms/{config["KEYCLOAK_REALM"]}/users'
    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/admin/realms/{config["KEYCLOAK_REALM"]}/users'

    #response variable is used to store the status code of the request
    response = requests.post(url, headers=admin_header, json=user)

    return response.status_code


def user_token_keycloak(username, password):
    """
    Returns the Token from the Keycloak server

    Parameters
    ----------
    username : str
        The username of the user
    password : str
        The password of the user

    Returns
    -------
    keycloak_token : str
        The token of the user. This token is used to authenticate the user.
        If keycloak_token is False, the user is not authenticated.
    """
    payload = {"grant_type": "password",
               "client_id": 'admin-cli',
               "client_secret": config['KEYCLOAK_REALM_SECRET']}
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br"
    }

    payload['password'] = password
    payload['username'] = username

    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/realms/{config["KEYCLOAK_REALM"]}/protocol/openid-connect/token'

    tokens = json.loads(
        requests.post(
            url,
            data=payload, headers=headers, verify=False
        ).content
    )
    try:
        keycloak_token = tokens['access_token']
        return keycloak_token
    except KeyError:
        return False


def get_attribute_keycloak(username):
    """
    This function is used to get the attributes of a user in the keycloak server

    Parameters
    ----------
    username : str
        username of the user

    Returns
    -------
    user_attributes : dict
        attributes of the user
    """
    #url variable is used to get the attributes of a user in the keycloak server
    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/auth/admin/realms/{config["KEYCLOAK_REALM"]}/users'
    #user_info variable is used to store the details of the user
    user_info = requests.get(
        f'{url}?username={username}', headers=get_admin_header_keycloak()
    ).json()[0]

    #if the user has attributes then it is stored in user_attributes variable
    if 'attributes' in user_info:
        user_attributes = json.loads(user_info['attributes']['resources'][0])
    #if the user does not have any attributes then user_attributes is set to empty
    else:
        user_attributes = []

    #return the user_attributes
    return user_attributes


def get_user_info(username):
    """
    This function is used to get the details of a user in the keycloak server

    Parameters
    ----------
    username : str
        username of the user

    Returns
    -------
    return_user : dict
        details of the user
    """
    #url variable is used to get the details of a user in the keycloak server
    url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/admin/realms/{config["KEYCLOAK_REALM"]}/users'
    #user variable is used to store the details of the user
    user = requests.get(
        f'{url}?username={username}', headers=get_admin_header_keycloak()
    ).json()[0]

    # transform the user info from keycloak to the user info used in the app
    return_user = {}
    return_user['id'] = user['id']
    return_user['username'] = user['username']
    return_user['email'] = user['email']
    return_user['first_name'] = user['firstName']
    return_user['last_name'] = user['lastName']
    #return the user
    return return_user


def get_user_info_from_token(token):
    
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br"
        }

    payload = {
        'client_id': 'admin-cli',
        'client_secret': config['KEYCLOAK_REALM_SECRET'],
        'token': token}
    
    keycloak_endpoint = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
        f'/realms/{config["KEYCLOAK_REALM"]}/protocol/openid-connect/token/introspect'

    try:
        response = requests.post(
            keycloak_endpoint, headers=headers, data=payload, verify=False
        )

        if response.status_code == 200:
            user_keycloak = response.json()
            user_info = {}
            user_info['id'] = user_keycloak['sub']
            user_info['username'] = user_keycloak['preferred_username']
            user_info['email'] = user_keycloak['email']
            user_info['first_name'] = user_keycloak['given_name']
            user_info['last_name'] = user_keycloak['family_name']
            return user_info
        else:
            return 'Could not validate credentials'
    except Exception as e:
        return 'Server error'


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = get_user_info_from_token(token)
    except:
        raise credentials_exception
    if isinstance(user, str):
        if user == 'Could not validate credentials':
            raise credentials_exception
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        return user
