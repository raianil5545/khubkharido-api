import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="Anil",
        last_name="Rai",
        email="anilrai@gmail.com",
        password="HereTest@",
        role="seller"
    )
    response = client.post("/api/user/register/", payload)
    data = response.data
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert "password" not in data
    assert data["email"] == payload["email"]


@pytest.mark.django_db
def test_login_user_pass(user_seller, client):
    response = client.post("/api/user/login/", dict(email="testseller@gmail.com", password="TestSeller",))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(user_buyer, client):
    """
    everytime test is called dataabse is destroyed and created so register first then login
    :return:
    """
    response = client.post("/api/user/login/", dict(email="testseller@gmail.com", password="TestSeller"))
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_user(user_seller, auth_client):
    response = auth_client.get('/api/user/getuser/')
    assert response.status_code == 200
    data = response.data
    assert data["id"] == user_seller.id
    assert data["email"] == user_seller.email


@pytest.mark.django_db
def test_logout(auth_client):
    response = auth_client.post('/api/user/logout/')

    assert response.status_code == 200
    assert response.data["message"] == "logged out"
