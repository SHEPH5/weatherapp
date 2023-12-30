from django.shortcuts import render
import requests
import datetime


def index(request):
    API_KEY = open("apikey", "r").read()
    current_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/oncecall?lat={}&lon={}&exclude=current,minutely,hourly,alert&appid={}"
    
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.get('city2', None)

        weather_data1, dailyforecast1 = fetch_weather[city1, API_KEY, current_url, forecast_url]

        if city2: 
            weather_data2, dailyforecast2 = fetch_weather[city2, API_KEY, current_url, forecast_url]
        else:
            weather_data2, dailyforecast2 = None, None
        
        context = {
            "weather_data1": weather_data1,
            "daily_forecast1": dailyforecast1,
            "weather_data2": weather_data2,
            "daily_forecast2": dailyforecast2,
        }
        return render(request, "base/homepage.html", context)

            
    else:
        render(request, 'base/homepage.html')


def fetch_weather(city, apikey, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, apikey)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']

    forecast_response = requests.get(forecast_url.format(lat, lon, apikey)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

    daily_forecast = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecast.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecast


