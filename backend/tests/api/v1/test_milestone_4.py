import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from app.models.user import User

def test_get_scenarios(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/scenarios/scenario_001/registry")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert data["id"] == "scenario_001"

def test_start_and_reset_scenario(client: TestClient, db):
    # Create a user to get a token
    from app.core.security import create_access_token
    # just create a fake user in db or we can mock deps.get_current_active_user
    
    # We will override the dependency instead
    from app.api import deps
    def override_get_current_active_user():
        return User(id="user-123", email="test@test.com", is_active=True)
    
    from app.main import app
    app.dependency_overrides[deps.get_current_active_user] = override_get_current_active_user

    try:
        # Start scenario
        res = client.post(
            f"{settings.API_V1_STR}/scenarios/scenario_001/start"
        )
        assert res.status_code == 200
        
        # Check state
        res = client.get(
            f"{settings.API_V1_STR}/scenarios/scenario_001/state"
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "IN_PROGRESS"
        
        # Hit vulnerable route
        res = client.post(
            f"{settings.API_V1_STR}/scenarios/scenario_001/vulnerable/auth/login?username=admin"
        )
        assert res.status_code == 200
        assert "token" in res.json()
        
        # Reset scenario
        res = client.post(
            f"{settings.API_V1_STR}/scenarios/scenario_001/reset"
        )
        assert res.status_code == 200
    finally:
        app.dependency_overrides.clear()
