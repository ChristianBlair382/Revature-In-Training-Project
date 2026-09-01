from tests.conftest import auth_header

async def test_login_succeeds_with_correct_credentials(client, seeded_users):
    response = await client.post(
        "/auth/token",
        data={"username": seeded_users["admin"].username, "password": "pw"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_login_fails_with_incorrect_credentials(client, seeded_users):
    response = await client.post(
        "/auth/token",
        data={"username": seeded_users["admin"].username, "password": "wrong"},
    )
    assert response.status_code == 401

async def test_register_requires_fleet_admin(client, seeded_users):
    payload = {"username": "new_user", "password": "somepass123", "role": "Field_Technician"}

    #assert that technician cannot perform this action
    technician_response = await client.post(
        "/auth/register", json=payload, headers=auth_header(seeded_users["technician"])
    )
    assert technician_response.status_code == 403

    #assert that admin can perform this action
    admin_response = await client.post(
        "/auth/register", json=payload, headers=auth_header(seeded_users["admin"])
    )
    assert admin_response.status_code == 201