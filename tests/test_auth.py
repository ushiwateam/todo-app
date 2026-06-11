def test_register_user(client):
    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 201
    assert "token" in response.json()


def test_register_duplicate_email(client, create_user):
    create_user(email="test@example.com")

    response = client.post("/register", json={
        "name": "user",
        "email": "test@example.com",
        "password": "dummypassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user(client, create_user):
    user_data = {
        "email": "test@example.com",
        "password": "dummypassword"
    }
    create_user(email=user_data["email"], password=user_data["password"])
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_non_existing_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "dummypassword"
    }
    response = client.post("/login", json=user_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Email inexistant ou mot de passe incorrect"


def test_login_bad_password(client, create_user):
    user_data = {
        "email": "test@example.com",
        "password": "badpassword"
    }
    create_user(email=user_data["email"], password="dummypassword")
    response = client.post("/login", json=user_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Email inexistant ou mot de passe incorrect"
