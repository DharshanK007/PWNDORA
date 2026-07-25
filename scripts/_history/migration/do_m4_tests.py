import os

test_content = '''import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_get_scenarios(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/scenarios/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == "scenario_001"

def test_start_and_reset_scenario(client: TestClient, superuser_token_headers: dict):
    # Start scenario
    res = client.post(
        f"{settings.API_V1_STR}/scenarios/scenario_001/start",
        headers=superuser_token_headers
    )
    assert res.status_code == 200
    
    # Check state
    res = client.get(
        f"{settings.API_V1_STR}/scenarios/scenario_001/state",
        headers=superuser_token_headers
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "IN_PROGRESS"
    
    # Hit vulnerable route
    res = client.post(
        f"{settings.API_V1_STR}/scenarios/scenario_001/vulnerable/auth/login?username=admin",
        headers=superuser_token_headers
    )
    assert res.status_code == 200
    assert "token" in res.json()
    
    # Reset scenario
    res = client.post(
        f"{settings.API_V1_STR}/scenarios/scenario_001/reset",
        headers=superuser_token_headers
    )
    assert res.status_code == 200
'''
with open("backend/tests/api/v1/test_milestone_4.py", "w") as f: f.write(test_content)

print("Created milestone 4 tests")
