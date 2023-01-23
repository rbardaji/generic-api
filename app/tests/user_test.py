from fastapi.testclient import TestClient

from ..main import app


def _delete_test_users(client):
    """
    Delete all test users and related data from KeyCloak and MongoDB.
    Tested endpoints:
    - DELETE /user/{user_id}
    - POST /token
    - GET /user/me
    """
    for username in ['test_user_1', 'test_user_2']:
        for password in ['test_password', 'updated_test_password']:
            # Get token from the username
            response = client.post(
                "/token", data={"username": username, "password": password}
            )
            if response.status_code == 200:
                token = response.json()["access_token"]
                # Get user_id from the username
                response = client.get(
                    f"/user/me", headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    user_id = response.json()["id"]
                    # Delete the test_user
                    client.delete(
                        f"/user/{user_id}",
                        headers={"Authorization": f"Bearer {token}"}
                    )

                    # Check if the test users were deleted
                    response = client.post(
                        "/token", 
                        data={
                            "username": username, "password": password
                        }
                    )
                    assert response.status_code == 401
                else:
                    assert False == f'Deleting {username}, could not get user_id'
    return True


def _create_test_users(client):
    """
    Creates a test_user_1 and a test_user_2
    """
    for username in ['test_user_1', 'test_user_2']:
        new_user = {
            "username": username,
            "password": "test_password",
            "email": f"{username}@test.com",
            "first_name": f"First name from {username}",
            "last_name": f"Last name from {username}"
        }
        response = client.post("/user", json=new_user)
        assert response.status_code == 201
        assert response.json()["username"] == username
        assert response.json()["email"] == f"{username}@test.com"
        assert response.json()["first_name"] == f"First name from {username}"
        assert response.json()["last_name"] == f"Last name from {username}"
    
    return True


def _update_test_user_1(client):
    """
    Updates test_user_1
    Tested endpoints:
    - POST /token
    - PUT /user/{user_id}
    - GET /user/me
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get user_id from test_user_1
    response = client.get(
        "/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    # Update test_user_1
    update_info_list = [
        {'first_name': 'Updated first name'},
        {'last_name': 'Updated last name'},
        {'email': 'updated_test_user_1@test.com'},
        {'password': 'updated_test_password'}
    ]
    for update_info in update_info_list:
        response = client.put(
            f"/user/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
            json=update_info
        )
        assert response.status_code == 204
        # Use the correct password
        if 'password' in update_info.keys():
            password = update_info.get('password')
        else:
            password = 'test_password'
        # Get the token again
        response = client.post(
            "/token",
            data={"username": "test_user_1", "password": password}
        )
        assert response.status_code == 200
        # Get the user info again if password was not updated
        if 'password' not in update_info.keys():
            token = response.json()["access_token"]
            response = client.get(
                f"/user/me", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert response.json()[list(update_info.keys())[0]] == update_info.get(
                list(update_info.keys())[0]
            )
    return True


def test_all_test():
    """
    In order to run the tests, connections to KeyCloak and MongoDB need to be
    established, which can take some time. To avoid delays, the connections to
    KeyCloak and MongoDB will only be made once, from a single function.
    From this function, all other tests will be called.

    Procedure:
    1. Delete all test users and related data from KeyCloak and MongoDB
        Tested endpoints:
        - POST /token
        - DELETE /user/{user_id}
        - GET /user/me
    2. Create a test users
        Tested endpoints:
        - POST /user
    3. Update a test_user_1
        Tested endpoints:
        - POST /token
        - PUT /user/{user_id}
        - GET /user/me
    Last. Delete all test users (again)
    """
    with TestClient(app) as client:
        # 1. Delete all test users and related data from KeyCloak and MongoDB
        _delete_test_users(client)
        # 2. Create a test user
        _create_test_users(client)
        # 3. Update a test_user_1
        _update_test_user_1(client)
        # Last. Delete all test users (again)
        _delete_test_users(client)