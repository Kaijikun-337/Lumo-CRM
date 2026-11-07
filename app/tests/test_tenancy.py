def test_multi_tenant_project_isolation(client):
    # Register and authenticate User A
    client.post("/api/v1/auth/register", json={"name": "User A", "email": "usera@lumo.dev", "password": "pass123"})
    res_a = client.post("/api/v1/auth/login", data={"username": "usera@lumo.dev", "password": "pass123"})
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register and authenticate User B
    client.post("/api/v1/auth/register", json={"name": "User B", "email": "userb@lumo.dev", "password": "pass123"})
    res_b = client.post("/api/v1/auth/login", data={"username": "userb@lumo.dev", "password": "pass123"})
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates a private project
    proj_a = client.post(
        "/api/v1/projects/",
        json={"name": "Alpha Confidential", "description": "Internal internal pipeline"},
        headers=headers_a
    ).json()
    proj_a_id = proj_a["id"]

    # User B attempts to fetch User A's project by ID -> 404 Not Found
    get_b = client.get(f"/api/v1/projects/{proj_a_id}", headers=headers_b)
    assert get_b.status_code == 404

    # User B lists projects -> empty array
    list_b = client.get("/api/v1/projects/", headers=headers_b).json()
    assert len(list_b) == 0

    # User A lists projects -> sees own project
    list_a = client.get("/api/v1/projects/", headers=headers_a).json()
    assert len(list_a) == 1
    assert list_a[0]["name"] == "Alpha Confidential"