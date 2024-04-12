from flask import url_for
from project.service.database import db
from project.models.users import User
import json
from unittest.mock import patch

def test_main_get(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_main_post(test_client):
    response = test_client.post('/')
    assert response.status_code == 200

def test_payment_without_user(test_client):
    response = test_client.get(url_for('main.payment'))
    assert response.status_code == 302
    assert 'Location' in response.headers
    assert '/login' in response.headers['Location']

def test_payment_with_user(test_client):
    response = test_client.get(url_for('main.payment'))
    response.set_cookie("user_info", f'username={"username"}')
    assert response.status_code == 302
    assert 'Location' in response.headers
    assert '/login' in response.headers['Location']

def test_pay(test_client, init_database):
    response = test_client.post('/payment')
    assert response.status_code == 302

def test_add_to_favourite_without_user(test_client):
    # Simulace parametrů požadavku
    location_name = "Praha"
    params = {'location': location_name}

    # Simulace požadavku na přidání do oblíbených
    response = test_client.get(url_for('main.add_to_favourite'), query_string=params)

    # Zkontrolujte, zda byl uživatel přesměrován na hlavní stránku s požadovanou lokalitou
    assert response.status_code == 302  # Přesměrování

def test_add_to_favourite_with_user(test_client, new_user):
    with patch('project.controllers.main_controller.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = new_user
        location_name = "Praha"
        params = {'location': location_name}
        response = test_client.get(url_for('main.add_to_favourite'), query_string=params)
        assert response.status_code == 302