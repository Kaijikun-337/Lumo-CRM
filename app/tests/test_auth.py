def test_register_and_login_flow(client):
    # 1. Register a new user
    reg_payload = {
        "name": "Alex Developer",
        "email": "alex@lumo.dev",
        "password": "securepassword123"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "alex@lumo.dev"
    assert "id" in user_data

    # 2. Reject registration with duplicate email
    dup_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
    assert dup_res.json()["detail"] == "User exists"  # Updated to match endpoint detail

    # 3. Successful login with correct credentials
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": "alex@lumo.dev", "password": "securepassword123"}
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 4. Reject login with wrong password
    bad_login_res = client.post(
        "/api/v1/auth/login",
        data={"username": "alex@lumo.dev", "password": "wrongpassword"}
    )
    assert bad_login_res.status_code == 401