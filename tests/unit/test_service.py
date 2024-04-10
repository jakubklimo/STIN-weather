from project.service.weather import get_weather, get_forecast, get_history, show_weather, current_location
from project.service.cookies import read_secure_cookie, delete_secure_cookie, create_secure_cookie, get_user
from flask import Response, request
import json

def test_get_weather():
    city = "Prague"
    weather_data = get_weather(city)
    assert 'error' not in weather_data

def test_get_forecast():
    city = "Prague"
    weather_data = get_forecast(city)
    assert 'error' not in weather_data

def test_get_history():
    city = "Prague"
    days_num = 7
    weather_history = get_history(city, days_num)
    assert isinstance(weather_history, list)

def test_show_weather():
    city = "Prague"
    weather_data, weather_forecast, weather_history, error, loc = show_weather(city)
    assert error is None

def test_create_secure_cookie(app):
    with app.test_request_context():
        username = "test_user"
        response = create_secure_cookie(username)

        assert isinstance(response, Response)

        assert 'user_info' in response.headers['Set-Cookie']
        assert 'HttpOnly' in response.headers['Set-Cookie']
        assert 'SameSite=Strict' in response.headers['Set-Cookie']
        assert 'Secure' not in response.headers['Set-Cookie']
        assert response.status_code == 302
        assert response.location == "/"

def test_delete_secure_cookie_with_valid_data(app):
    with app.test_request_context():
        # Simulace běžící aplikace Flask a získání odpovědi z funkce delete_secure_cookie
        response = delete_secure_cookie()

        # Ověření, že funkce vrací objekt odpovědi
        assert response is not None

        # Ověření, že byla nastavena cookie "user_info" s parametrem expires=0
        assert "Set-Cookie" in response.headers
        assert "user_info=; Expires=Thu, 01 Jan 1970 00:00:00 GMT" in response.headers["Set-Cookie"]

        # Ověření, že odpověď přesměrovává na správnou cílovou URL
        assert response.status_code == 302
        assert response.location == "/"

def test_read_secure_cookie(app):
    with app.test_request_context():
        response = read_secure_cookie()
        assert response == None

def test_get_user_with_existing_name(init_database):
    user = get_user("testUser")

    assert user.name == "testUser"

def test_get_user_with_non_existing_name():
    user = get_user("non_existing_user")

    assert user is None

def test_current_location():
    result = current_location()
    assert result == None