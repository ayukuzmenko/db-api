from .test_setup import client


def test_health_check() -> None:
    response = client.get("/health")
    assert (
        response.status_code == 200
    ), "Expected status code 200, got {response.status_code}"
    assert response.json() == {"status": "Ok", "message": "Service is up and running."}
