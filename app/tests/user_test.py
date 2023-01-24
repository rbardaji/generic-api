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


def _update_test_user_2_with_test_user_1_token(client):
    """
    Tries to update test_user_2 with the token from test_user_1
    Tested endpoints:
    - POST /token
    - PUT /user/{user_id}
    """
    # Get token from test_user_1
    # CAUTION: At this point, test_user_1 has already been updated with a new
    # password
    response = client.post(
        "/token",
        data={"username": "test_user_1", "password": "updated_test_password"}
    )
    assert response.status_code == 200
    token_user_1 = response.json()["access_token"]
    # Get token from test_user_2
    response = client.post(
        "/token", data={"username": "test_user_2", "password": "test_password"}
    )
    assert response.status_code == 200
    token_user_2 = response.json()["access_token"]
    # Get user_id from test_user_2
    response = client.get(
        "/user/me", headers={"Authorization": f"Bearer {token_user_2}"}
    )
    assert response.status_code == 200
    user_2_id = response.json()["id"]
    # Try to update test_user_2 with the token from test_user_1
    response = client.put(
        f"/user/{user_2_id}",
        headers={"Authorization": f"Bearer {token_user_1}"},
        json={"first_name": "Updated first name"}
    )
    assert response.status_code == 403
    return True


def _delete_test_user_2_with_test_user_1_token(client):
    """
    Tries to update test_user_2 with the token from test_user_1
    Tested endpoints:
    - POST /token
    - PUT /user/{user_id}
    """
    # Get token from test_user_1
    # CAUTION: At this point, test_user_1 has already been updated with a new
    # password
    response = client.post(
        "/token",
        data={"username": "test_user_1", "password": "updated_test_password"}
    )
    assert response.status_code == 200
    token_user_1 = response.json()["access_token"]
    # Get token from test_user_2
    response = client.post(
        "/token", data={"username": "test_user_2", "password": "test_password"}
    )
    assert response.status_code == 200
    token_user_2 = response.json()["access_token"]
    # Get user_id from test_user_2
    response = client.get(
        "/user/me", headers={"Authorization": f"Bearer {token_user_2}"}
    )
    assert response.status_code == 200
    user_2_id = response.json()["id"]
    # Try to delete test_user_2 with the token from test_user_1
    response = client.delete(
        f"/user/{user_2_id}",
        headers={"Authorization": f"Bearer {token_user_1}"}
    )
    assert response.status_code == 403
    return True


def _get_all_users(client):
    """
    Get all users
    Tested endpoints:
    - GET /user
    """
    # Get token from test_user_2
    response = client.post(
        "/token", data={"username": "test_user_2", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all users with the token from test_user_2
    response = client.get(
        "/user", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # Try to get all users without a token
    response = client.get("/user")
    assert response.status_code == 401
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
    2. Create the test users
        Tested endpoints:
        - POST /user
    3. Update a test_user_1
        Tested endpoints:
        - POST /token
        - PUT /user/{user_id}
        - GET /user/me
    4. Try to update the test_user_2 with the token from test_user_1
        Tested endpoints:
        - POST /token
        - PUT /user/{user_id}
    5. Try to delete the test_user_2 with the token from test_user_1
        Tested endpoints:
        - POST /token
        - DELETE /user/{user_id}
    6. Get the list from all users with and without a valid token
    Last. Delete all test users (again)
    """
    with TestClient(app) as client:
        # 1. Delete all test users and related data from KeyCloak and MongoDB
        _delete_test_users(client)
        # 2. Create a test user
        _create_test_users(client)
        # 3. Update a test_user_1
        _update_test_user_1(client)
        # 4. Try to update the test_user_2 with the token from test_user_1
        _update_test_user_2_with_test_user_1_token(client)
        # 5. Try to delete the test_user_2 with the token from test_user_1
        _delete_test_user_2_with_test_user_1_token(client)
        # 6. Get the list from all users with and without a valid token
        _get_all_users(client)
        # Last. Delete all test users (again)
        _delete_test_users(client)
