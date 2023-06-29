from django.shortcuts import render 
import json 
import urllib.request
import datetime

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
