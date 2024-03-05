from fastapi.testclient import TestClient

from db_api.main import app

client = TestClient(app)
