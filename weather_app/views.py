from django.shortcuts import render, redirect, HttpResponse
import requests
from django.http import JsonResponse
from .models import City
from django.contrib import messages

def home(request):

    API_key = '78e30d34c9d02f9f1aea568d7c901390'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        city_name = request.POST.get('city')
        respond = requests.get(url.format(city_name, API_key)).json()
        if respond['cod'] == 200:
            if not City.objects.filter(name=city_name).exists():
                City.objects.create(name=city_name)
                messages.success(request, f'{city_name} has been added successfully!.')
            else:
                messages.info(request, f'{city_name} already exists!.')
        else:
            messages.error(request, f'City {city_name} not found!.')
        return redirect('home')
        
    weater_data = []
    try:
        cities = City.objects.all()
        for city in cities:
            respond = requests.get(url.format(city.name, API_key))
            data = respond.json()

            if data['cod'] == 200:
                city_weather = {
                    'city' : city.name,
                    'temperature' : data['main']['temp'],
                    'description' : data['weather'][0]['description'],
                    'icon' : data['weather'][0]['icon']
                }
                weater_data.append(city_weather)
            else:
                City.objects.filter(name = city.name).delete()
    except requests.RequestException as e:
        print('Error connceting to weather service. Please try again later.')

    context = {'weather_data':weater_data}

    return render(request, 'index.html', context)