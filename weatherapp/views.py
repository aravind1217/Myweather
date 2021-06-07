from django.shortcuts import render,redirect
from django.contrib import messages
import requests
import json
from django.http import HttpResponse
from .models import City
from .forms import Cityform
from django.contrib.auth.decorators import login_required

@login_required
def Homeview(request):
       
	url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=Your APi key "
	" You can get your API key form registering here https://openweathermap.org/"

	if request.method == "POST":
		form = Cityform(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			city_count = City.objects.filter(name = new_city).count()
			if city_count == 0:
				obj = requests.get(url.format(new_city)).json()
				if obj['cod'] == 200:
					form.save()
				else:
				    messages.error(request,f'city is not found')

			else:
			    messages.error(request,f'Already city added')
		else:
			messages.error(request,f'city added')

				
		
	   
	form = Cityform()
	weather = []
    
	city = City.objects.all()
	for i in city:
		obj = requests.get(url.format(i)).json()
		print(obj)
		city_weather = {
		  'city':i,
		  "country":obj['sys']['country'],
		  'temperature':obj['main']['temp'],
		  'description':obj['weather'][0]['description'],
		  'icon' :obj['weather'][0]['icon'],
		  'main':obj['weather'][0]['main'],
		  'pressure'   :obj['main']['pressure'],

          




		}
		weather.append(city_weather)
		print(weather)
	context ={
	'weather':weather,'form':form}
	return render(request,"base.html",context)

def City_Delete(request,city_name):
	City.objects.get(name= city_name).delete()
	return redirect('home')

