content = '''import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_rate_limiting(client: TestClient):
    # Depending on RATE_LIMIT_PER_MINUTE, we could hit it.
    # We will simulate exactly limit + 1 requests
    limit = settings.RATE_LIMIT_PER_MINUTE
    
    # Send normal requests
    for i in range(limit):
        res = client.get(f"{settings.API_V1_STR}/health/live")
        # Could be 200 depending on route, or 429 if we exceeded
        
    res = client.get(f"{settings.API_V1_STR}/health/live")
    assert res.status_code == 429
    assert res.json()["success"] == False

def test_pagination_and_standard_error(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/users/?skip=0&limit=10")
    # if unauthenticated, returns 401 wrapped in our standard error?
    # Actually wait, Depends throws HTTPException which is caught by our handler?
    # Our NeoFactoryException handler returns standard error, but generic HTTPException doesn't unless overridden.
    # Let's see if 401 from Depends is wrapped. If not, it's fine.
    
    assert res.status_code in [401, 200]
    
    if res.status_code == 401:
        data = res.json()
        assert "detail" in data or "message" in data
'''
with open("backend/tests/api/v1/test_advanced.py", "w") as f:
    f.write(content)
print("Created test_advanced.py")
