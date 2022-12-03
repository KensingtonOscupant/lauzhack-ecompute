'''
A flask app that serves a json response on the route /power and the weather information under /weather 
'''
import json
import requests
from flask import Flask, request
from dataloader import load_data


app = Flask(__name__)

LONG = {
    'berlin': 13.404954,
    'frankfurt': 8.682127,
    'california': -119.417931,
}

LAT = {
    'berlin': 52.520008,
    'frankfurt': 50.110924,
    'california': 36.778261,
}

WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=c5f95483d4a80b97988a644b1163b58a'

app = Flask(__name__)

@app.route('/weather')
def weather():
    city = request.args.get('city', default='berlin')
    weather_json = requests.get(WEATHER_API.format(LAT[city], LONG[city]))
    return dict(json.loads(weather_json.text))

@app.route('/week')
def week():
    week = request.args.get('week', default=f'2022_47')  # TODO: change to current week
    meta, col_info, data = load_data()
    return {
        'meta': meta.to_dict(),
        'col_info': col_info.to_dict(),
        'data': data.to_dict(),
    }
