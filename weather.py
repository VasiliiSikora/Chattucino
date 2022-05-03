from map import location_get
import json
import requests

def weather_get(location):
    [latitude, longitude] = location_get(location)
    KEY = '8af340833e58a324b6848fbbe2296849'
    lat = latitude
    lon = longitude
    part = 'minutely,hourly,alerts'
    API_URL_json = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&units=metric&appid={KEY}'

    response = requests.get(API_URL_json)
    data=json.loads(response.text)

    return data

