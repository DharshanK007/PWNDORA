content = '''import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_get_company(client: TestClient):
    # Depending on auth, might need to login
    # Login first
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "ceo@neofactory.com", "password": "password123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get(f"{settings.API_V1_STR}/company/", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "NeoFactory Industries"

def test_get_dashboard_summary(client: TestClient):
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "ceo@neofactory.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get(f"{settings.API_V1_STR}/dashboard/summary", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "employees" in data
    assert "assets" in data

def test_get_scenarios(client: TestClient):
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "ceo@neofactory.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get(f"{settings.API_V1_STR}/scenarios/", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
'''
with open("backend/tests/api/v1/test_milestone_3d.py", "w") as f:
    f.write(content)

print("Created test_milestone_3d.py")
