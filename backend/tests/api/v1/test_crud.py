from app.core.config import settings

def test_create_department(client, db):
    # Need admin token
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@neofactory.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    
    response = client.post(
        f"{settings.API_V1_STR}/departments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Dept", "description": "Testing"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Dept"
