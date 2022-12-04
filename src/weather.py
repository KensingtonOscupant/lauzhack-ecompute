import json
import requests


OPEN_WEATHER_MAP_API_KEY = "c5f95483d4a80b97988a644b1163b58a"
CITY_API = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}'
WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'

KELVIN_OFFSET = -273.15

def get_weather(city):
    city_data = requests.get(CITY_API.format(city, OPEN_WEATHER_MAP_API_KEY))
    city_dict = json.loads(city_data.text)[0]
    lat, lon = city_dict['lat'], city_dict['lon']
    weather_data = requests.get(WEATHER_API.format(lat, lon, OPEN_WEATHER_MAP_API_KEY))
    weather_dict = json.loads(weather_data.text)
    return {
        'main': weather_dict['weather'][0]['main'],  # general description
        'temp': weather_dict['main']['temp'] + KELVIN_OFFSET,  # celsius (after conversion)
        'clouds': weather_dict['clouds']['all'],  # percent
        'wind': weather_dict['wind']['speed'],  # meters / second
        'humidity': weather_dict['main']['humidity'],  # percent
        'pressure': weather_dict['main']['pressure'],  # hectopascals
    }
