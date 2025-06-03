from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.contrib import messages
import logging

from .services import WeatherService

logger = logging.getLogger(__name__)

def dashboard(request):
    """
    Main dashboard view displaying current weather conditions and forecast
    """
    weather_service = WeatherService()
    weather_data = weather_service.fetch_current_conditions()
    forecast_data = weather_service.fetch_forecast(days=3)  # 3-day forecast
    
    context = {
        'weather': weather_data,
        'forecast': forecast_data,
        'station_name': weather_data.get('station_name', 'Personal Weather Station') if weather_data else 'Personal Weather Station',
    }
    
    if not weather_data:
        context['error_message'] = "Unable to fetch weather data at this time."
    
    return render(request, 'weather/dashboard.html', context)

def forecast_view(request):
    """
    Detailed forecast view
    """
    weather_service = WeatherService()
    forecast_data = weather_service.fetch_forecast(days=3)  # 3-day forecast only
    
    context = {
        'forecast': forecast_data,
        'page_title': 'Weather Forecast'
    }
    
    if not forecast_data:
        context['error_message'] = "Unable to fetch forecast data at this time."
    
    return render(request, 'weather/forecast.html', context)

def map_view(request):
    """
    Map view showing weather station location
    """
    context = {
        'page_title': 'Weather Station Map',
        'station_lat': 65.6835,  # Personal station coordinates (approximate Iceland location)
        'station_lng': -18.1262,
        'station_name': 'Personal Weather Station'
    }
    
    return render(request, 'weather/map.html', context)

@require_http_methods(["GET"])
@cache_page(60 * 2)  # Cache for 2 minutes
def api_current_weather(request):
    """
    API endpoint for getting current weather data as JSON
    """
    weather_service = WeatherService()
    weather_data = weather_service.fetch_current_conditions()
    
    if weather_data:
        return JsonResponse({
            'success': True,
            'data': weather_data
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Unable to fetch weather data'
        }, status=503)

@require_http_methods(["GET"])
@cache_page(60 * 5)  # Cache for 5 minutes
def api_forecast(request):
    """
    API endpoint for getting forecast data as JSON
    """
    weather_service = WeatherService()
    days = request.GET.get('days', 3)
    try:
        days = int(days)
        days = min(max(days, 1), 3)  # Limit between 1 and 3 days
    except (ValueError, TypeError):
        days = 3
    
    forecast_data = weather_service.fetch_forecast(days=days)
    
    if forecast_data:
        return JsonResponse({
            'success': True,
            'data': forecast_data
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Unable to fetch forecast data'
        }, status=503)

def about(request):
    """
    About page with information about the weather station
    """
    context = {
        'station_name': 'Personal Weather Station',
        'page_title': 'About'
    }
    return render(request, 'weather/about.html', context)
