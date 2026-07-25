import os

tests_dir = "backend/tests/api/v1"

test_workflows = '''from app.core.config import settings

def test_employee_workflow(client, db):
    # Need admin token
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@neofactory.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create Department
    dept_res = client.post(
        f"{settings.API_V1_STR}/departments/",
        headers=headers,
        json={"name": "Engineering"}
    )
    dept_id = dept_res.json()["id"]
    
    # 2. Create User
    user_res = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
        json={"email": "emp@neofactory.com", "password": "pass", "role": "Employee"}
    )
    user_id = user_res.json()["id"]
    
    # 3. Create Employee
    emp_res = client.post(
        f"{settings.API_V1_STR}/employees/",
        headers=headers,
        json={"first_name": "John", "last_name": "Doe", "department_id": dept_id, "user_id": user_id}
    )
    emp_id = emp_res.json()["id"]
    
    assert emp_res.json()["status"] == "Pending"
    
    # 4. Activate Employee
    act_res = client.post(
        f"{settings.API_V1_STR}/employees/{emp_id}/activate",
        headers=headers
    )
    assert act_res.status_code == 200
    assert act_res.json()["status"] == "Active"

    # 5. Terminate Employee
    term_res = client.post(
        f"{settings.API_V1_STR}/employees/{emp_id}/terminate",
        headers=headers
    )
    assert term_res.status_code == 200
    assert term_res.json()["status"] == "Terminated"
    
    # 6. Try to activate terminated (should fail)
    fail_res = client.post(
        f"{settings.API_V1_STR}/employees/{emp_id}/activate",
        headers=headers
    )
    assert fail_res.status_code == 400

def test_inventory_workflow(client, db):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@neofactory.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create Inventory
    inv_res = client.post(
        f"{settings.API_V1_STR}/inventory/",
        headers=headers,
        json={"component_name": "Sensor A", "part_number": "SN-100", "stock_quantity": 10}
    )
    inv_id = inv_res.json()["id"]
    assert inv_res.json()["status"] == "Created"
    
    # 2. Allocate Inventory (qty 5)
    alloc_res = client.post(
        f"{settings.API_V1_STR}/inventory/{inv_id}/allocate",
        headers=headers,
        json={"quantity": 5}
    )
    assert alloc_res.status_code == 200
    assert alloc_res.json()["status"] == "Allocated"
    assert alloc_res.json()["stock_quantity"] == 5
    
    # 3. Consume Inventory
    cons_res = client.post(
        f"{settings.API_V1_STR}/inventory/{inv_id}/consume",
        headers=headers
    )
    assert cons_res.status_code == 200
    assert cons_res.json()["status"] == "Consumed"
'''

with open(f"{tests_dir}/test_workflows.py", "w") as f:
    f.write(test_workflows)
print("Tests generated")
