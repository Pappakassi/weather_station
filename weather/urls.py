from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('forecast/', views.forecast_view, name='forecast'),
    path('map/', views.map_view, name='map'),
    path('api/current/', views.api_current_weather, name='api_current'),
    path('api/forecast/', views.api_forecast, name='api_forecast'),
    path('about/', views.about, name='about'),
] 