"""
A flask app that serves a json response on the route /power and the weather information under /weather 
"""
from flask import Flask, request
import requests


app = Flask(__name__)

long = {
    'berlin': 13.404954,
    'frankfurt': 8.682127,
    'california': -119.417931,
}

lat = {
    'berlin': 52.520008,
    'frankfurt': 50.110924,
    'california': 36.778261,
}

@app.route('/weather')
def weather():
    city = request.args.get('city', 'berlin')

    f = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat[city]}=&lon={lon[city]}&appid=c5f95483d4a80b97988a644b1163b58a')
