from fastapi.testclient import TestClient

from ..main import app


def _stats_test(client):
    """
    Test the GET /stats endpoint.
    """
    response = client.get("/stats")
    assert response.status_code == 200
    return True


def test_all_test():
    """
    In order to run the tests, connections to KeyCloak and MongoDB need to be
    established, which can take some time. To avoid delays, the connections to
    KeyCloak and MongoDB will only be made once, from a single function.
    From this function, all other tests will be called.

    Procedure:
    1. Check that GET /stats returns 200
    """
    with TestClient(app) as client:
        # 1. Check that GET /stats returns 200
        _stats_test(client)
