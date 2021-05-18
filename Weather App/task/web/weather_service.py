import datetime

import requests
from requests.exceptions import RequestException

API_KEY = "69c56eeb6775b9eebe832cf96cf7e4f7"


def get_current_weather(city, city_id):
    """Get weather conditions from openweathermap.org using api"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    weather_conditions = {}
    try:
        response = requests.post(url, data={"city": city})
        response.raise_for_status()
        weather = response.json()
        current_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=weather.get('timezone'))
        hours = int(current_time.strftime("%H"))

        if hours < 6 or hours > 20:
            time_class = "card night"
        elif 6 < hours < 12 or 17 < hours < 20:
            time_class = "card evening-morning"
        else:
            time_class = "card day"

        weather_conditions['time_class'] = time_class
        weather_conditions['timezone'] = weather.get('timezone')
        weather_conditions['city'] = city
        weather_conditions['temp'] = weather.get('main').get('temp')
        weather_conditions['weather_state'] = weather.get('weather')[0].get('main')
        weather_conditions['id'] = city_id
    except RequestException:
        pass
    return weather_conditions


def check_city(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.post(url, data={"city": city})
    print(response.status_code)

    if response.status_code != 200:
        return False
    return True
