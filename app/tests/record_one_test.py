import dotenv

from fastapi.testclient import TestClient

from app.main import app
from .user_test import _delete_test_users, _create_test_users
from .record_two_test import _delete_test_records, _create_test_records, \
    _check_no_records_user_one

# Import the dotenv library to load environment variables from .env file
config = dotenv.dotenv_values(".env")


def _delete_test_records_one(client):
    """
    Deletes all resources from the database
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    resource_list = response.json()
    for resource in resource_list:
        # Delete all resources that were created by test_user_1
        if resource["owner"] == "test_user_1":
            # Delete all resources with the token from test_user_1
            response = client.delete(
                f"/{config['RECORD_ONE_NAME']}/{resource['id']}",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 204
    return True


def _create_test_records_one(client):
    """
    Creates two records with the token from test_user_1
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Create a record with the token from test_user_1
    new_record = {
        "title": "test_record",
        "visible": True,
    }
    response = client.post(
        f"/{config['RECORD_ONE_NAME']}",
        json=new_record,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == new_record["title"]
    assert response.json()["visible"] == new_record["visible"]
    # Create the second record with the token from test_user_1
    new_record = {
        "title": "test_record_2",
        "visible": True,
    }
    response = client.post(
        f"/{config['RECORD_ONE_NAME']}",
        json=new_record,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == new_record["title"]
    assert response.json()["visible"] == new_record["visible"]
    return True


def _check_no_records_one_user_one(client):
    """
    Check that test_user_1 has no records
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == []


def _check_two_records_user_one(client, check_connection=False):
    """
    Check that test_user_1 has no records
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    if check_connection:
        assert len(response.json()[0]["connections"]) == 1


def _check_records_user_one(client):
    """
    Check that test_user_1 has no records
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def _check_records_no_token(client):
    """
    Check that are records
    """
    # Get token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}",
    )
    assert response.status_code == 200
    record_list = response.json()
    # Check that there is a record with title "test_record"
    for record in record_list:
        if record["title"] == "test_record":
            return True
    assert False


def _update_test_record(client):
    """
    Updates a record with the token from test_user_1
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    resource_list = response.json()
    # Get the id from the record with title "test_record"
    record_id = None
    for resource in resource_list:
        if resource["title"] == "test_record":
            record_id = resource["id"]
            break
    assert record_id is not None
    # Retrieve the record_two with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_TWO_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    resource_list = response.json()
    # Get the id from the record with title "test_record"
    record_two_id = None
    for resource in resource_list:
        if resource["title"] == "test_record":
            record_two_id = resource["id"]
            break
    assert record_two_id is not None
    # Update the record with the token from test_user_1
    new_record = {
        "title": "test_record_updated",
        "visible": False,
        "connections": [
            {
                "id": record_two_id,
                "title": "test_record",
                "type": config["RECORD_TWO_NAME"]
            }
        ]
    }
    response = client.put(
        f"/{config['RECORD_ONE_NAME']}/{record_id}",
        json=new_record,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["visible"] == new_record["visible"]
    return True


def _check_no_records_no_token(client):
    """
    Check that are no test records
    """
    # Get token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}",
    )
    assert response.status_code == 200
    record_list = response.json()
    print(record_list)
    # Check that there is a record with title "test_record"
    for record in record_list:
        if record["title"] == "test_record":
            assert False
    return True


def _check_no_records_user_two(client):
    """
    Check that test_user_2 has no records
    """
    # Get token from test_user_2
    response = client.post(
        "/token", data={"username": "test_user_2", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_2
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == []
    return True


def _check_record_user_one_filtered_by_title(client):
    """
    Check that test_user_1 has one records filtered by title
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}/me?title=2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def _check_records_user_one_filtered_by_title(client):
    """
    Check that test_user_1 has two records filtered by title
    """
    # Get token from test_user_1
    response = client.post(
        "/token", data={"username": "test_user_1", "password": "test_password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    # Get all resources with the token from test_user_1
    response = client.get(
        f"/{config['RECORD_ONE_NAME']}?title=2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_all_test():
    """
    In order to run the tests, connections to KeyCloak and MongoDB need to be
    established, which can take some time. To avoid delays, the connections to
    KeyCloak and MongoDB will only be made once, from a single function.
    From this function, all other tests will be called.

    1. Delete all test users and related data from KeyCloak and MongoDB
        Tested endpoints:
        - POST /token
        - DELETE /user/{user_id}
        - GET /user/me
    2. Create the test users
        Tested endpoints:
        - POST /user
    3. Delete all test records
        Tested endpoints:
        - POST /token
        - DELETE /record/{record_id}
    4. Check that test_user_1 has no records
        Tested endpoints:
        - POST /token
        - GET /record/me
    5. Delete all test records two
        Tested endpoints:
        - POST /token
        - GET /record_two/me
        - DELETE /record_two/{record_id}
    6. Check that test_user_1 has no record_two
        Tested endpoints:
        - POST /token
        - GET /record_two/me
    7. Create two records_two with the token from test_user_1
        Tested endpoints:
        - POST /token
        - POST /record_two    
    8. Create two records with the token from test_user_1
        Tested endpoints:
        - POST /token
        - POST /record
    9. Check that test_user_1 has two records
        Tested endpoints:
        - POST /token
        - GET /record/me
    10. Check that the record exists when get the list of records with the token
        from test_user_1
        Tested endpoints:
        - POST /token
        - GET /record
    11. Check that the record exists when get the list of records with the token
        filtered by title
        Tested endpoints:
        - POST /token
        - GET /record
    12. Check that the record exists when get the list of records without a token
        Tested endpoints:
        - GET /record
    13. Update the record with the token from test_user_1
        Tested endpoints:
        - POST /token
        - PUT /record/{record_id}
    14. Check that test_user_1 has two record
        Tested endpoints:
        - POST /token
        - GET /record/me
    15. Check that test_user_1 has one record if it is filtered by title
        Tested endpoints:
        - POST /token
        - GET /record/me
    16. Check that the record not exists when get the list of records without a
        token
        Tested endpoints:
        - GET /record
    17. Check that the record does not exists when get the list of records with 
        the token from test_user_2
        Tested endpoints:
        - POST /token
        - GET /record/me
    Pre-last. Delete all test records (again)
    Last. Delete all test users (again)
    """
    with TestClient(app) as client:
        # 1. Delete all test users and related data from KeyCloak and MongoDB
        _delete_test_users(client)
        # 2. Create a test user
        _create_test_users(client)
        # 3. Delete all test records
        _delete_test_records_one(client)
        # 4. Check that test_user_1 has no records
        _check_no_records_one_user_one(client)
        # 5. Delete all test record_two
        _delete_test_records(client)
        # 6. Check that test_user_1 has no record_two
        _check_no_records_user_one(client)
        # 7. Create two records_two with the token from test_user_1
        _create_test_records(client)
        # 8. Create two record with the token from test_user_1
        _create_test_records_one(client)
        # 9. Check that test_user_1 has two record
        _check_two_records_user_one(client)
        # 10. Check that the record exists when get the list of records with the
        # token from test_user_1
        _check_records_user_one(client)
        # 11. Check that the record exists when get the list of records with the
        # token filtered by title
        _check_records_user_one_filtered_by_title(client)
        # 12. Check that the record exists when get the list of records without a
        # token
        _check_records_no_token(client)
        # 13. Update the visibility of the record
        _update_test_record(client)
        # 14. Check that test_user_1 has two record
        _check_two_records_user_one(client, check_connection=True)
        # 15. Check that test_user_1 has one record if it is filtered by title
        _check_record_user_one_filtered_by_title(client)
        # 16. Check that the record not exists when get the list of records
        # without a token
        _check_no_records_no_token(client)
        # 17. Check that the record does not exists when get the list of records
        # with the token from test_user_2
        _check_no_records_user_two(client)
        # Pre-last. Delete all test resources (again)
        _delete_test_records_one(client)
        _delete_test_records(client)
        # Last. Delete all test users (again)
        _delete_test_users(client)
