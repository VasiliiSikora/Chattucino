#Using Bing Maps

API_KEY = 'AoqFXS5Ki1QMFt0XF-02zhn_5CJBBSBRy4EHGrPKHBzMe0uQGXT87m1Kp3Hw4xI1'

locationQuery = '25/1 Gatehouse Drive Kensington'.replace(' ','%20')
includeNeighborhood = 0
maxResults = 10


map_URL = f'http://dev.virtualearth.net/REST/v1/Locations?query={locationQuery}&includeNeighborhood={includeNeighborhood}&maxResults={maxResults}&key={API_KEY}'

[lon,lat] = map_URL['resourceSets']['resources']['point']['coordinates']