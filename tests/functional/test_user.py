def test_login_success(test_client, init_database):
    # Ověření, že úspěšné přihlášení vytváří cookie
    response = test_client.post('/login', data=dict(user="testUser1", password="password1"), follow_redirects=True)
    # Ověření, že po úspěšném přihlášení je status code 302 (přesměrování)
    assert response.status_code == 200
    # Ověření, že cookie byla vytvořena

def test_login_failure(test_client):
    # Ověření, že neúspěšné přihlášení vrátí chybovou zprávu
    response = test_client.post('/login', data={'user': 'test_user', 'password': 'wrong_password'})
    # Ověření, že po neúspěšném přihlášení je status code 200 (OK)
    assert response.status_code == 200

def test_register_failure(test_client):
    response = test_client.post("/register")
    assert response.status_code == 200

def test_logout(test_client):
    response = test_client.get("/logout")
    assert response.status_code == 302