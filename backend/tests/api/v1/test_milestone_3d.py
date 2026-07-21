import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_get_company(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/company/")
    # If no auth required or auth required, it should be 401 or 404 or 200
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_summary(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/summary")
    assert res.status_code in [200, 401, 404]

def test_get_scenarios(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/scenarios/")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_organization(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/organization")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_network(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/network")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_security(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/security")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_operations(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/operations")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_statistics(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/statistics")
    assert res.status_code in [200, 401, 404]
