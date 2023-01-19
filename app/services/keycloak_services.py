import json
import requests
from dotenv import dotenv_values
from keycloak import KeycloakOpenID, exceptions, KeycloakAdmin

#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


# keycloak_url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}'
# print('-------------------')
# print('-------------------')
# print(keycloak_url)

# keycloak_admin = KeycloakAdmin(server_url=keycloak_url,
#                                username=config['KEYCLOAK_ADMIN'],
#                                password=config['KEYCLOAK_ADMIN_PASSWORD'],
#                                realm_name="master",
#                                user_realm_name=config["KEYCLOAK_REALM"],
#                                client_secret_key=config["KEYCLOAK_ADMIN_SECRET"],
#                                verify=True)

# def create_user_keycloak(username, first_name, last_name, email, password):
#     """
#     This function is used to create a new user in the keycloak server

#     Parameters
#     ----------
#     username : str
#         username of the new user
#     first_name : str
#         first name of the new user
#     last_name : str
#         last name of the new user
#     email : str
#         email of the new user
#     password : str
#         password of the new user

#     Returns
#     -------
#     int
#         status code of the request
#     """
#     # Add user
#     new_user = keycloak_admin.create_user(
#         {
#             "email": email,
#             "username": username,
#             "enabled": True,
#             "firstName": first_name,
#             "lastName": last_name,
#             "credentials": [
#                 {
#                     "value": password,
#                     "type": "password"
#                 }
#             ]
#         }
#     )

#     return new_user











# Client configuration
keycloak_url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}'
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_url,
    client_id='admin-cli',
    realm_name=config["KEYCLOAK_REALM"],
    client_secret_key=config["KEYCLOAK_ADMIN_SECRET"],
    verify=False
)


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
               "client_secret": config['KEYCLOAK_ADMIN_SECRET']}
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



def check():
    import requests

    # Your Keycloak token
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJqd3NpVmVrLVh3cVYtc2d2ckR2R1I2Q2t1cFZjdVR5cVVtYzI5Y0VHdzNRIn0.eyJqdGkiOiJjZGVmODM3Mi1mYjYwLTQ2ZDQtOWFhYS1jN2U4Y2QyMjE2MzYiLCJleHAiOjE1OTE3MjgxMjcsIm5iZiI6MCwiaWF0IjoxNTkxNzI3ODI3LCJpc3MiOiJodHRwczovL2tleWNsb2FrLmlvL2F1dGgvcmVhbG1zL2V4YW1wbGUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMzI2ZDY4YzgtMzllYi00OTI4LTkyMzAtMjVlMGE3ZjE3ZjEyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYWNjb3VudCIsImF1dGhfdGltZSI6MCwic2Vzc2lvbl9zdGF0ZSI6ImQ2N2M2OTc5LTU2N2EtNDA5NS04NzNjLTU1YjNlMzU1MjU3OSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9leGFtcGxlLmNvbSJdLCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX0sInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1leGFtcGxlQGV4YW1wbGUuY29tIiwiY2xpZW50SG9zdCI6IjE5Mi4xNjguMS4xMjUiLCJjbGllbnRJRCI6ImFjY291bnQifQ.fnnJ4zjh4X9bGzI2QY_jKlSf-cxBVZ-Od3qUz7VU9m6d1T6uYT6U-BVjf2F-Z7GgPk-N4GkyX9M4yEbRf1FQI1wVc_Lxk-7oq3-dFxiJzt9hb3vKzW3ql8r87k-5hxrjvRZW_f2hC7VXSkzfE_yVYM0HpP0hA-gJfFZVHJE8nAi7hXQ-a-VHGKcYmfVwcFxhvZV44ConMs8E1-hJ9t-Lmlpj49qW8qr5r_P5NxZM_f1ceQN4KlD9X4GPGfL-Ou2QS1VwIcxFvsaVh3qdnsgUz7XU6B22_V7L-6Tf0s7KM2xvHVbPuG0q3-Aq-_oVZvKep1xiSVzfQRmi9RVOV4N4MjIw"

    # Your Keycloak Server URL
    keycloak_url = "https://keycloak.io/auth/realms/example/protocol/openid-connect/token/introspect"

    # Building the request
    request_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer "+token
    }

    # Sending the request
    response = requests.post(keycloak_url, data="token="+token, headers=request_headers)

    # Checking the response
    if response.status_code == 200:
        print("Token is valid")
    else:
        print("Token is invalid")
    

    import requests 

    keycloak_endpoint = 'https://www.example.com/auth/realms/master/protocol/openid-connect/userinfo'

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

    headers = {'Authorization': 'Bearer ' + token}

    try:
        response = requests.get(keycloak_endpoint, headers=headers)

        if response.status_code == 200:
            print('Token es valido')
            user_info = response.json()
            print('Informacion del usuario: ' + str(user_info))
        else:
            print('Token no es valido')
    except Exception as e:
        print('Error al comprobar el token: ' + str(e))


# def get_user_info_from_token_keycloak(username, token):

#     payload_final = {
#         'client_id': 'admin-cli',
#         'client_secret': config['KEYCLOAK_REALM_SECRET'],
#         "username": username,
#         'token': token}
    
#     headers = {
#         "Connection": "keep-alive",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br"
#     }

#     url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
#         f'/realms/{config["KEYCLOAK_REALM"]}/protocol/openid-connect/token/introspect'
#     # url = f'{config["KEYCLOAK_URL"]}:{config["KEYCLOAK_PORT"]}' + \
#     #     f'/realms/master/protocol/openid-connect/token/introspect'
#     print('url', url)

#     response = requests.post(
#         url, data=payload_final, headers=headers, verify=False
#     )
#     print('response status', response.status_code)
#     print('response content', response.content)

#     data = json.loads(
#         requests.post(
#             url,
#             data=payload_final, headers=headers, verify=False).content)
#     return data


# def get_user_info_from_token_keycloak(token):
#     """
#     Returns the user info from the token

#     Parameters
#     ----------
#     token : str
#         The token of the user

#     Returns
#     -------
#     user_id : str
#         The user id of the user
#     """
#     user_keycloak = keycloak_openid.userinfo(token)
#     print('-------------------------------')
#     print(user_keycloak)
#     try:
#         user_keycloak = keycloak_openid.userinfo(token)
#         print('-------------------------------')
#         print(user_keycloak)
#         user_info = {}
#         user_info['_id'] = user_keycloak['sub']
#         user_info['name'] = user_keycloak['given_name']
#         user_info['surname'] = user_keycloak['family_name']
#         user_info['email'] = user_keycloak['email']
#         user_info['username'] = user_keycloak['preferred_username']
        
#         user_info['resources'] = get_attribute_keycloak(
#             user_keycloak['preferred_username']
#         )
#         return user_info
#     except exceptions.KeycloakAuthenticationError:
#         return False
