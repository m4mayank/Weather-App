import requests
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, TemplateView, DeleteView
from . import models
from .models import City, SelectedCity
from .forms import CityForm
from django.http import Http404
from django.contrib.auth import get_user_model
import os

# Create your views here.
User = get_user_model()
class IndexView(TemplateView):
    template_name='weather/index.html'

class WeatherListView(LoginRequiredMixin, CreateView):
    form_class = CityForm
    model = SelectedCity
    success_url = reverse_lazy('weather:weather')
    template_name = 'weather/weather.html'

    def get_form_kwargs(self):
        kwargs = super(WeatherListView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form_class):
        self.object = form_class.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form_class)

    def get_context_data(self, **kwargs):
        API_KEY=os.getenv('api_key')
        url = "http://api.openweathermap.org/data/2.5/weather?q={name}&units=imperial&appid={api}"
        try:
            cities = SelectedCity.objects.prefetch_related('user').filter(user_id__exact = self.request.user.id)
        except User.DoesNotExist:
            raise Http404
        else:
            weather_data = []
            for city in cities:
                r = requests.get(url.format(name=city.city, api=str(API_KEY))).json()
                print(r)
                city_weather = {
                    'id': city.id,
                    'city' : city.city.name,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                }
                weather_data.append(city_weather)
        context = super().get_context_data(**kwargs)
        context['weather_data']=weather_data
        return context 


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'weather/city_dropdown_list_options.html', {'cities': cities})


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = models.SelectedCity
    success_url = reverse_lazy('weather:weather')
