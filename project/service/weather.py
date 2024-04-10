from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import request
import requests
import os

def get_api_key():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    return api_key


def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={get_api_key()}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data

def get_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={get_api_key()}&q={city}&days=7"
    response = requests.get(url)
    data = response.json()
    return data

def get_history(city, days_num):
    end_dt = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    dt = ((datetime.now() - timedelta(days=1)) - timedelta(days=days_num)).strftime('%Y-%m-%d')
    url = f"http://api.weatherapi.com/v1/history.json?key={get_api_key()}&q={city}&dt={dt}&end_dt={end_dt}"

    response = requests.get(url)
    data = response.json()

    filtered_data = []
    if 'forecast' in data and 'forecastday' in data['forecast']:
        for forecast_day in data['forecast']['forecastday']:
            for hour_forecast in forecast_day['hour']:
                if hour_forecast['time'].endswith('12:00'):
                    filtered_data.append(hour_forecast)
    return filtered_data

def show_weather(city):
    weather_data = get_weather(city)
    weather_forecast = get_forecast(city)
    weather_history = get_history(city, 7)
    if 'error' in weather_data or 'error' in weather_forecast:
        error = weather_data['error']['message']
    else:
        error = None
    return weather_data, weather_forecast, weather_history, error, city

def current_location():
    try:
        ip_address = request.remote_addr
        if ip_address == '127.0.0.1':
            city_name = "Prague"
            return show_weather(city_name)
        else:
            response = requests.get(f"https://ipinfo.io/%7Bip_address%7D/json")
            if response.status_code == 200:
                data = response.json()
                city_name = data.get("city")
                return show_weather(city_name)
            else:
                return None
    except Exception as e:
        print("Error:", e)
        return None
