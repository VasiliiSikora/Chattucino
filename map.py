#Using Bing Maps
import json
import requests
from flask import jsonify

def location_get(location):
    API_KEY = 'AoqFXS5Ki1QMFt0XF-02zhn_5CJBBSBRy4EHGrPKHBzMe0uQGXT87m1Kp3Hw4xI1'

    locationQuery = location.replace(' ','%20')

    map_URL = f'http://dev.virtualearth.net/REST/v1/Locations?query={locationQuery}&includeNeighborhood=0&maxResults=10&key={API_KEY}'

    response = requests.get(map_URL)
    data=json.loads(response.text)

    [lat,lon] = data['resourceSets'][0]['resources'][0]['point']['coordinates']

    return ["{:.6f}".format(lat), "{:.6f}".format(lon)]

def static_map_get(location):
    [lat, lon] = location_get(location)
    API_KEY = 'AoqFXS5Ki1QMFt0XF-02zhn_5CJBBSBRy4EHGrPKHBzMe0uQGXT87m1Kp3Hw4xI1'
    map_URL = f'https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/{lat},{lon}/16?mapSize=400,400&pp={lat},{lon}&key=AoqFXS5Ki1QMFt0XF-02zhn_5CJBBSBRy4EHGrPKHBzMe0uQGXT87m1Kp3Hw4xI1'

    return map_URL

    


