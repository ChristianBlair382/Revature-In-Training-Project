from tests.conftest import auth_header

# The admin has full CRUD Permissions, and can thus edit the status of any given service_call
async def test_operations_admin_can_update_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/service_call/{seeded_service_call.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"

# The technician doesn't have full CRUD Permissions, but should still have permission to edit the status of any given service_call
async def test_field_technician_can_update_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/service_call/{seeded_service_call.id}/status",
        json={"status": "Failed"},
        headers=auth_header(seeded_users["technician"]),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Failed"

# The auditor can only view data, but can't modify it, so they shouldn't have permission to edit a service_call's status.
async def test_auditor_cannot_update_status(client, seeded_users, seeded_service_call):
    response = await client.patch(
        f"/service_calls/service_call/{seeded_service_call.id}/status",
        json={"status": "Failed"},
        headers=auth_header(seeded_users["auditor"]),
    )
    assert response.status_code == 403

# Missions that don't have existing entrees should return a 404 error when looked up.
async def test_nonexistent_service_call_returns_404(client, seeded_users):
    response = await client.patch(
        f"/service_calls/service_call/69420/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )
    assert response.status_code == 404