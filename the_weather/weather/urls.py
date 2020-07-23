from django.urls import path, re_path
from . import views
app_name = 'weather'
urlpatterns = [
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('', views.IndexView.as_view(), name='home'),
    path('weather/', views.WeatherListView.as_view(), name = "weather"),
    #re_path(r'weather/(?P<slug>[-\w]+)/$', views.CityDeleteView.as_view(), name='delete'),
    re_path(r'^weather/(?P<pk>\d+)/delete/$', views.CityDeleteView.as_view(), name='delete'),
]