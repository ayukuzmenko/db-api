from .test_setup import client


def test_read_items() -> None:
    response = client.get("/api/select")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Response should be a list"

    for item in data:
        assert "id" in item and isinstance(
            item["id"], int
        ), "Each item should have an 'id' field of type int"
        assert "value" in item and isinstance(
            item["value"], str
        ), "Each item should have a 'value' field of type str"


def test_create_item() -> None:
    test_data = {"value": "test value"}
    response = client.post("/api/insert", json=test_data)
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code}"

    data = response.json()
    assert "id" in data and isinstance(
        data["id"], int
    ), "Item should have an 'id' field of type int"
    assert "value" in data and isinstance(
        data["value"], str
    ), "Item should have a 'value' field of type str"
    assert (
        test_data["value"] == data["value"]
    ), "Ensure the returned 'value' field matches the value sent in the request."


def test_delete_item() -> None:
    test_data = {"value": "test value"}
    response_create = client.post("/api/insert", json=test_data)
    created_item = response_create.json()

    response = client.delete(f"/api/delete/{created_item['id']}")
    assert (
        response.status_code == 204
    ), f"Expected status code 204, got {response.status_code}"
