from django.shortcuts import render, redirect 
import json 
import urllib.request
import datetime
from .models import cityname
from .forms import cityForm
from django.contrib import messages
import requests 

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        base_url = 'https://api.openweathermap.org/data/2.5/weather?'
        api_key = 'eb0b6d2eb8a38f1e1fd9687c39ef8de8'
        #Replace with your valid API key from OpenWeatherMap
        res = urllib.request.urlopen(base_url + 'appid=' + api_key + '&q=' + city).read()        
        json_data = json.loads(res)
        temp= json_data['main']['temp']
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinates": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
            
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
            "desp":str(json_data['weather'][0]['description']),
            "icon":str(json_data['weather'][0]['icon']),
            "day":str(datetime.date.today()),
            "te":str(datetime.datetime.now())
        }
        return render(request, 'index.html', {'data':data,'city':city,'temp':temp})
    else:
        data = {}
        return render(request, 'index.html', {'data':data})  


import requests


def context(request):
    if request.method == 'POST':
        form=cityForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("City has been added"))
            return redirect('context')
    else:
        ticker = cityname.objects.all()
        output = []
        base_url = 'https://api.openweathermap.org/data/2.5/weather?'
        api_key = 'eb0b6d2eb8a38f1e1fd9687c39ef8de8'

        for ticker_item in ticker:
            api_request = requests.get(base_url + 'appid=' + api_key + '&q=' + str(ticker_item))

            try:
                api = json.loads(api_request.content)
                output.append(api)
                
                for item in output:
                    sunset_unix_timestamp = item['sys']['sunset']
                    sunset_datetime_utc = datetime.datetime.utcfromtimestamp(sunset_unix_timestamp)
                    item['sunset_time'] = sunset_datetime_utc.strftime('%H:%M:%S')

                    sunrise_unix_timestamp = item['sys']['sunrise']
                    sunrise_datetime_utc = datetime.datetime.utcfromtimestamp(sunrise_unix_timestamp)
                    item['sunrise_time'] = sunrise_datetime_utc.strftime('%H:%M:%S')

            except Exception as e:
                api = "Error...."

        return render(request, 'context.html', {'ticker': ticker, 'output': output})



def delete_city(request,city_name):
    ticker=cityname.objects.get(pk=city_name)
    ticker.delete
    messages.success(request,("City has been deleted! "))
    return redirect('context')
    