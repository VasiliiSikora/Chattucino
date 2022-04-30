KEY = '96617311f71c4bf3b0d44922223004'
# API_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&units=metric&appid={KEY}'

location = 'Kensington'
date = '2022-05-02'

API_URL= f'http://api.weatherapi.com/v1/forecast.json?key={KEY}?q={location}?dt={date}'
print(API_URL)