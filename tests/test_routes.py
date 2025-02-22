import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    print(response.data)  # Lägg till denna rad för att se exakt vad som returneras
    expected_output = "Hello, Flask! (Refaktorerad)"
    assert response.status_code == 200
    assert response.data == expected_output  # Uppdatera testet