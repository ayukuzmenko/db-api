from .test_setup import client


def test_transaction_bad_request() -> None:
    response = client.post("/api/commit")
    error_msg = (
        "Expected status code 400 for commit without an active transaction, "
        "got {}. Ensure API correctly handles commit requests without an "
        "active transaction."
    )
    assert response.status_code == 400, error_msg.format(response.status_code)

    response = client.post("/api/rollback")
    error_msg = (
        "Expected status code 400 for rollback without an active transaction, "
        "got {}. Ensure API correctly handles rollback requests without an "
        "active transaction."
    )
    assert response.status_code == 400, error_msg.format(response.status_code)


def test_transaction() -> None:
    error_msg = "Expected status code {}, got {}"

    # Begin the transaction
    response_begin = client.post("/api/begin")
    assert response_begin.status_code == 200, error_msg.format(
        200, response_begin.status_code
    )

    data_begin = response_begin.json()
    assert data_begin == {
        "message": "transaction started"
    }, "Transaction did not start as expected"

    # Insert data in the context of the transaction
    test_data_1 = {"value": "test value"}
    response_create = client.post("/api/insert", json=test_data_1)
    assert response_create.status_code == 201, error_msg.format(
        201, response_create.status_code
    )
    data_create = response_create.json()

    assert "id" in data_create, "Insert response does not contain id"

    # Check data before the transaction is commited
    response_read = client.get("/api/select")
    assert response_read.status_code == 200, error_msg.format(
        200, response_read.status_code
    )
    data_read = response_read.json()
    assert not any(
        item["id"] == data_create["id"] for item in data_read
    ), "Data should not be visible before commit"

    # Commit the transaction
    response_commit = client.post("/api/commit")
    assert response_commit.status_code == 200, error_msg.format(
        200, response_commit.status_code
    )
    data_commit = response_commit.json()
    assert data_commit == {
        "message": "transaction committed"
    }, "Transaction did not commit as expected"

    # Check data after the transaction is committed
    response_read_after_commit = client.get("/api/select")
    assert response_read_after_commit.status_code == 200, error_msg.format(
        200, response_read_after_commit.status_code
    )
    data_read_after_commit = response_read_after_commit.json()
    assert any(
        item["id"] == data_create["id"] for item in data_read_after_commit
    ), "Data should be visible after commit"


def test_rollback_transaction() -> None:
    error_msg = "Expected status code {}, got {}"

    # Begin the transaction
    response_begin = client.post("/api/begin")
    assert response_begin.status_code == 200, error_msg.format(
        200, response_begin.status_code
    )

    # Insert data in the context of the transaction
    test_data = {"value": "test value for rollback"}
    response_insert = client.post("/api/insert", json=test_data)
    assert response_insert.status_code == 201, error_msg.format(
        201, response_insert.status_code
    )
    data_insert = response_insert.json()

    # Check selected data
    response_select_before_commit = client.get("/api/select")
    assert response_select_before_commit.status_code == 200, error_msg.format(
        200, response_select_before_commit.status_code
    )
    data_select_before_commit = response_select_before_commit.json()
    assert not any(
        item["value"] == test_data["value"] for item in data_select_before_commit
    ), "Inserted data should not be visible before commit"

    # Rollback the transaction
    response_rollback = client.post("/api/rollback")
    assert response_rollback.status_code == 200, error_msg.format(
        200, response_rollback.status_code
    )

    data_rollback = response_rollback.json()
    assert data_rollback == {
        "message": "transaction rolled back"
    }, "Transaction did not rollback as expected"

    # Check data after the transaction is rolled back
    response_select_after_rollback = client.get("/api/select")
    assert response_select_after_rollback.status_code == 200, error_msg.format(
        200, response_select_after_rollback.status_code
    )
    data_select_after_rollback = response_select_after_rollback.json()
    assert not any(
        item["id"] == data_insert["id"] for item in data_select_after_rollback
    ), "Data inserted in the transaction should not be visible after rollback"


def test_nested_transaction() -> None:
    error_msg = "Expected status code {}, got {}"

    # Begin the first transaction
    response_begin1 = client.post("/api/begin")
    assert response_begin1.status_code == 200, error_msg.format(
        200, response_begin1.status_code
    )

    data_begin1 = response_begin1.json()
    expected_message = {"message": "transaction started"}
    assert (
        data_begin1 == expected_message
    ), "First transaction did not start as expected"

    # Begin the nested transaction
    response_begin2 = client.post("/api/begin")
    assert response_begin2.status_code == 200, error_msg.format(
        200, response_begin2.status_code
    )
    data_begin2 = response_begin2.json()
    assert (
        data_begin2 == expected_message
    ), "Nested transaction did not start as expected"

    # Insert data in the context of the nested transaction
    test_data_nested = {"value": "nested test value"}
    response_create_nested = client.post("/api/insert", json=test_data_nested)
    assert response_create_nested.status_code == 201, error_msg.format(
        201, response_create_nested.status_code
    )
    data_create_nested = response_create_nested.json()
    assert (
        "id" in data_create_nested
    ), "Insert response within nested transaction does not contain id"

    # Attempt to read data - should not be visible yet
    response_read_before_commit = client.get("/api/select")
    assert response_read_before_commit.status_code == 200, error_msg.format(
        200, response_read_before_commit.status_code
    )
    data_read_before_commit = response_read_before_commit.json()
    condition_before_commit = any(
        item["id"] == data_create_nested["id"] for item in data_read_before_commit
    )
    assert not condition_before_commit, (
        "Data inserted in nested transaction should not be visible "
        "before the outer transaction is committed"
    )
    # Commit the nested transaction
    response_commit_nested = client.post("/api/commit")
    assert response_commit_nested.status_code == 200, error_msg.format(
        200, response_commit_nested.status_code
    )
    data_commit_nested = response_commit_nested.json()
    assert data_commit_nested == {
        "message": "transaction committed"
    }, "Nested transaction did not commit as expected"

    # Data still should not be visible
    response_read_after_nested_commit = client.get("/api/select")
    assert response_read_after_nested_commit.status_code == 200, error_msg.format(
        200, response_read_after_nested_commit.status_code
    )
    data_read_after_nested_commit = response_read_after_nested_commit.json()
    condition_before_commit = any(
        item["id"] == data_create_nested["id"] for item in data_read_after_nested_commit
    )
    assert not condition_before_commit, (
        "Data inserted in nested transaction should not be visible "
        "before the outer transaction is committed"
    )

    # Commit the first (outer) transaction
    response_commit1 = client.post("/api/commit")
    assert response_commit1.status_code == 200, error_msg.format(
        200, response_commit1.status_code
    )

    data_commit1 = response_commit1.json()
    assert data_commit1 == {
        "message": "transaction committed"
    }, "First transaction did not commit as expected"

    # Check data after the transaction is committed
    response_read_after_commit = client.get("/api/select")
    assert response_read_after_commit.status_code == 200, error_msg.format(
        200, response_read_after_commit.status_code
    )
    data_read_after_commit = response_read_after_commit.json()
    condition_after_commit = any(
        item["id"] == data_create_nested["id"] for item in data_read_after_commit
    )
    assert condition_after_commit, (
        "Data inserted in nested transaction should be visible "
        "after both transactions are committed"
    )


def test_dirty_read() -> None:
    error_msg = "Expected status code {}, got {}"

    # Begin the transaction
    response_begin = client.post("/api/begin")
    assert response_begin.status_code == 200, error_msg.format(
        200, response_begin.status_code
    )
    test_data = {"value": "test value for dirty read"}

    # Insert data in the context of the transaction
    response_insert = client.post("/api/insert", json=test_data)
    assert response_insert.status_code == 201, error_msg.format(
        201, response_insert.status_code
    )

    # Check selected data without dirty read
    response_select_before_commit = client.get("/api/select")
    assert response_select_before_commit.status_code == 200, error_msg.format(
        200, response_select_before_commit.status_code
    )
    data_select_before_commit = response_select_before_commit.json()
    assert not any(
        item["value"] == test_data["value"] for item in data_select_before_commit
    ), "Inserted data should not be visible before commit"

    # Check selected data with dirty read
    response_select_before_commit = client.get(
        "/api/select", params={"is-dirty-read": True}
    )
    assert response_select_before_commit.status_code == 200, error_msg.format(
        200, response_select_before_commit.status_code
    )
    data_select_before_commit = response_select_before_commit.json()
    assert any(
        item["value"] == test_data["value"] for item in data_select_before_commit
    ), "Inserted data should be visible before commit"

    # Rollback the transaction
    response_rollback = client.post("/api/rollback")
    assert response_rollback.status_code == 200, error_msg.format(
        200, response_rollback.status_code
    )

    data_rollback = response_rollback.json()
    assert data_rollback == {
        "message": "transaction rolled back"
    }, "Transaction did not rollback as expected"
