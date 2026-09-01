from tests.conftest import auth_header

# This endpoint can't be reached without credentials
async def test_list_atms_requires_auth(client):
    response = await client.get("/atms")
    assert response.status_code == 401

# If an auditor can successfully read this endpoint, then any higher role can by proxy.
async def test_list_atms_any_auth_role(client, seeded_users):
    response = await client.get("/atms", headers=auth_header(seeded_users["auditor"]))
    assert response.status_code == 200

# Operators aren't allowed to create new atm entrees.
async def test_create_robot_forbidden_for_field_op(client, seeded_users, seeded_branch):
    payload = {
        "serial_num": "test_serial",
        "model": "test_model",
        "cash_lvl": 50,
        "branch_id": seeded_branch.id,
        "status": "Operational",
    }

    response = await client.post("/atms", json=payload, headers=auth_header(seeded_users["technician"]))
    assert response.status_code == 403

# Fleet Admins are allowed to create new robot entrees.
async def test_create_robot_succeeds_for_fleet_admin(client, seeded_users, seeded_branch):
    payload = {
        "serial_num": "test_serial",
        "model": "test_model",
        "cash_lvl": 50,
        "branch_id": seeded_branch.id,
        "status": "Operational",
    }

    response = await client.post("/atms", json=payload, headers=auth_header(seeded_users["admin"]))
    assert response.status_code == 201
    assert response.json()["serial_num"] == "test_serial"

async def test_verify_cash_lvl_within_constraints(client, seeded_users, seeded_branch):
    admin_headers = auth_header(seeded_users["admin"])
    low = {
        "serial_num": "test_serial_1",
        "model": "test_model",
        "cash_lvl": 10,
        "branch_id": seeded_branch.id,
        "status": "Operational",
    }
    high = {
        "serial_num": "test_serial_2",
        "model": "test_model",
        "cash_lvl": 90,
        "branch_id": seeded_branch.id,
        "status": "Operational",
    }

    await client.post("/atms", json=low, headers=admin_headers)
    await client.post("/atms", json=high, headers=admin_headers)

    response = await client.get("/atms?max_cash=20", headers=admin_headers)
    serials = [robot["serial_num"] for robot in response.json()]

    assert "test_serial_1" in serials
    assert "test_serial_2" not in serials