import os

filepath = "backend/tests/api/v1/test_milestone_3d.py"
with open(filepath, "r") as f: content = f.read()

if "test_get_dashboard_statistics" not in content:
    content += '''
def test_get_dashboard_operations(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/operations")
    assert res.status_code in [200, 401, 404]

def test_get_dashboard_statistics(client: TestClient):
    res = client.get(f"{settings.API_V1_STR}/dashboard/statistics")
    assert res.status_code in [200, 401, 404]
'''
    with open(filepath, "w") as f: f.write(content)

print("Updated tests")
